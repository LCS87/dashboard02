"""
Módulo de anonimização automática de dados sensíveis.
Implementa mascaramento de CNPJ, CPF, nomes e substituição de marcas.
"""
import re
import hashlib
from typing import Optional
from faker import Faker
import pandas as pd


class DataAnonymizer:
    """
    Anonimizador de dados sensíveis para uso em ambientes acadêmicos/demo.
    
    Características:
    - Determinístico: mesmo input sempre gera mesmo output (seed-based)
    - Cache de nomes para consistência
    - Mascaramento de CNPJ/CPF
    - Anonimização de nomes próprios
    - Substituição de marcas/empresas
    """
    
    def __init__(self, seed: int = 42):
        """
        Inicializa o anonimizador.
        
        Args:
            seed: Seed para reprodutibilidade (default: 42)
        """
        self.faker = Faker('pt_BR')
        Faker.seed(seed)
        self._seed = seed
        self.name_map: dict = {}  # Cache: original -> anonimizado
        self.company_map: dict = {}  # Cache de empresas
        
    def mask_cnpj(self, cnpj: str) -> str:
        """
        Mascara CNPJ mantendo apenas os 8 primeiros dígitos.
        Ex: 12.345.678/0001-90 -> 12.345.678/****-**
        """
        if pd.isna(cnpj) or not cnpj:
            return cnpj
            
        clean = re.sub(r'\D', '', str(cnpj))
        if len(clean) == 14:
            return f"{clean[:2]}.{clean[2:5]}.{clean[5:8]}/****-**"
        return cnpj
    
    def mask_cpf(self, cpf: str) -> str:
        """
        Mascara CPF mantendo apenas os 6 primeiros dígitos.
        Ex: 123.456.789-00 -> 123.456.***-**
        """
        if pd.isna(cpf) or not cpf:
            return cpf
            
        clean = re.sub(r'\D', '', str(cpf))
        if len(clean) == 11:
            return f"{clean[:3]}.{clean[3:6]}.***-**"
        return cpf
    
    def anonymize_name(self, name: str) -> str:
        """
        Gera nome fictício consistente baseado no hash do nome original.
        Mesmo nome sempre retorna o mesmo nome anonimizado.
        """
        if pd.isna(name) or not name or not str(name).strip():
            return name
            
        name_str = str(name).strip()
        
        # Cache hit
        if name_str in self.name_map:
            return self.name_map[name_str]
        
        # Gera seed determinístico a partir do nome
        name_hash = int(hashlib.md5(name_str.encode()).hexdigest(), 16)
        # Usa seed combinado para variedade mas determinismo
        combined_seed = (self._seed + name_hash) % (2**32)
        Faker.seed(combined_seed)
        
        # Gera nome fictício
        fake_name = self.faker.name()
        
        # Cache
        self.name_map[name_str] = fake_name
        
        return fake_name
    
    def anonymize_company(self, company: str) -> str:
        """
        Anonimiza nome de empresa de forma consistente.
        """
        if pd.isna(company) or not company or not str(company).strip():
            return company
            
        company_str = str(company).strip()
        
        if company_str in self.company_map:
            return self.company_map[company_str]
            
        company_hash = int(hashlib.md5(company_str.encode()).hexdigest(), 16)
        combined_seed = (self._seed + company_hash + 1000) % (2**32)
        Faker.seed(combined_seed)
        
        # Gera nome de empresa fictício
        fake_company = self.faker.company()
        
        self.company_map[company_str] = fake_company
        return fake_company
    
    def mask_phone(self, phone: str) -> str:
        """
        Mascara telefone mantendo DDD.
        Ex: (11) 99999-8888 -> (11) 9****-8888
        """
        if pd.isna(phone) or not phone:
            return phone
            
        clean = re.sub(r'\D', '', str(phone))
        if len(clean) >= 10:
            ddd = clean[:2]
            rest = clean[2:]
            if len(rest) == 9:
                return f"({ddd}) {rest[:1]}****-{rest[-4:]}"
            elif len(rest) == 8:
                return f"({ddd}) {rest[:4]}-****"
        return phone
    
    def mask_email(self, email: str) -> str:
        """
        Mascara email mantendo domínio.
        Ex: joao@empresa.com -> j****@empresa.com
        """
        if pd.isna(email) or not email or '@' not in str(email):
            return email
            
        local, domain = str(email).split('@', 1)
        if len(local) <= 1:
            return email
        masked_local = local[0] + '*' * (len(local) - 1)
        return f"{masked_local}@{domain}"
    
    def anonymize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica anonimização completa ao DataFrame.
        
        Colunas tratadas:
        - CNPJ_CLIENTE: mascara CNPJ
        - CNPJ: mascara CNPJ
        - CPF: mascara CPF
        - DIRETOR, GERENTE_DIVISAO, NOMEDIRETOR, NOMEGERENTEDIVISAO: anonimiza nomes
        - CLIENTE: anonimiza parcialmente
        - DEALER: anonimiza empresa
        - NM_TELEFONE: mascara telefone
        - EMAIL: mascara email
        - Substitui "Vivo" por "Telecomunicações S/A" em todas as colunas de texto
        """
        df = df.copy()
        
        # CNPJ
        for col in ['CNPJ_CLIENTE', 'CNPJ']:
            if col in df.columns:
                df[col] = df[col].apply(self.mask_cnpj)
        
        # CPF
        for col in ['CPF', 'CPF_CLIENTE']:
            if col in df.columns:
                df[col] = df[col].apply(self.mask_cpf)
        
        # Nomes de pessoas
        name_cols = ['DIRETOR', 'GERENTE_DIVISAO', 'NOMEDIRETOR', 'NOMEGERENTEDIVISAO']
        for col in name_cols:
            if col in df.columns:
                df[col] = df[col].apply(self.anonymize_name)
        
        # Cliente (parcial)
        if 'CLIENTE' in df.columns:
            df['CLIENTE'] = df['CLIENTE'].apply(
                lambda x: f"Cliente-***{str(x)[-3:]}" if pd.notna(x) and len(str(x)) > 3 else x
            )
        
        # Dealer/Empresa
        if 'DEALER' in df.columns:
            df['DEALER'] = df['DEALER'].apply(self.anonymize_company)
        
        # Telefone
        if 'NM_TELEFONE' in df.columns:
            df['NM_TELEFONE'] = df['NM_TELEFONE'].apply(self.mask_phone)
        
        # Email
        for col in ['EMAIL', 'EMAIL_CLIENTE']:
            if col in df.columns:
                df[col] = df[col].apply(self.mask_email)
        
        # Substituir marca "Vivo" em todas as colunas de texto (sem converter NaN/None para string)
        text_cols = df.select_dtypes(include=['object']).columns
        for col in text_cols:
            # Aplica replace apenas em valores não-nulos
            mask = df[col].notna()
            df.loc[mask, col] = df.loc[mask, col].astype(str).str.replace(
                'Vivo', 'Telecomunicações S/A', case=False, regex=False
            ).str.replace(
                'VIVO', 'Telecomunicações S/A', case=False, regex=False
            )
        
        return df
    
    def get_anonymization_report(self) -> dict:
        """
        Retorna relatório do que foi anonimizado.
        """
        return {
            'names_anonymized': len(self.name_map),
            'companies_anonymized': len(self.company_map),
            'name_samples': dict(list(self.name_map.items())[:5]),
            'company_samples': dict(list(self.company_map.items())[:5]),
        }


def create_anonymizer(seed: int = 42) -> DataAnonymizer:
    """Factory function para criar anonimizador."""
    return DataAnonymizer(seed=seed)


# Exemplo de uso e testes
if __name__ == "__main__":
    anonymizer = DataAnonymizer(seed=42)
    
    # Testes
    print("=== Testes de Anonimização ===\n")
    
    # CNPJ
    cnpj_test = "12.345.678/0001-90"
    print(f"CNPJ: {cnpj_test} -> {anonymizer.mask_cnpj(cnpj_test)}")
    
    # CPF
    cpf_test = "123.456.789-00"
    print(f"CPF: {cpf_test} -> {anonymizer.mask_cpf(cpf_test)}")
    
    # Nomes (testar determinismo)
    name_test = "João Silva Santos"
    print(f"Nome: {name_test} -> {anonymizer.anonymize_name(name_test)}")
    print(f"Nome (2ª vez): {name_test} -> {anonymizer.anonymize_name(name_test)}")
    
    # Empresa
    company_test = "Vivo Telecomunicações"
    print(f"Empresa: {company_test} -> {anonymizer.anonymize_company(company_test)}")
    
    # Telefone
    phone_test = "(11) 99999-8888"
    print(f"Telefone: {phone_test} -> {anonymizer.mask_phone(phone_test)}")
    
    # Email
    email_test = "joao.silva@empresa.com"
    print(f"Email: {email_test} -> {anonymizer.mask_email(email_test)}")
    
    # DataFrame
    test_df = pd.DataFrame({
        'CNPJ_CLIENTE': ['12.345.678/0001-90', '98.765.432/0001-10'],
        'CLIENTE': ['João Silva', 'Maria Santos'],
        'DIRETOR': ['Carlos Diretor', 'Ana Gerente'],
        'DEALER': ['Vivo Dealer 1', 'Vivo Dealer 2'],
        'NM_TELEFONE': ['(11) 99999-8888', '(21) 88888-7777'],
    })
    
    print("\n=== DataFrame Original ===")
    print(test_df)
    
    anon_df = anonymizer.anonymize_dataframe(test_df)
    print("\n=== DataFrame Anonimizado ===")
    print(anon_df)
    
    print("\n=== Relatório ===")
    print(anonymizer.get_anonymization_report())