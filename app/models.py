  
  
        
class Clients(db.Model):
    
    
    """
    Classe responsável por gerenciar o banco de dados do sistema.
    Essa Model é fixa, só deve ser alterada caso seja alterado algo de 
    configuração no database MySQL
    """
    
    
    __tablename__ = 'clients_table'
    id = db.Column(db.Integer, primary_key=True)
    name_client = db.Column(db.String(length=60), nullable=False, unique=True)
    cpf_cnpj = db.Column(db.String(length=30), nullable=False, unique=True)
    email_admin = db.Column(db.String(length=50), nullable=False, unique=True)
    bots_per_license = db.Column(db.Text, nullable=False)
    license_token = db.Column(db.String(length=512), nullable=False, unique=True)
    
    @property
    def senhacrip(self):
        return self.senhacrip
    
    @senhacrip.setter
    def senhacrip(self, senha_texto):
        self.license_token = bcrypt.hashpw(senha_texto.encode(), salt2).decode("utf-8")

    def converte_senha(self, senha_texto_claro):
        return bcrypt.checkpw(senha_texto_claro.encode("utf-8"), self.license_token.encode("utf-8"))