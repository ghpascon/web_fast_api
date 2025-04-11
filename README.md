# 🔐 Sistema Web com FastAPI, Autenticação e Banco de Dados

Este projeto é uma aplicação web desenvolvida com **FastAPI**, que possui:

- Sistema de autenticação com login
- Proteção de rotas para usuários autenticados
- Validação CSRF para formulários
- Conexão com banco de dados via SQLAlchemy
- Interface HTML renderizada com Jinja2
- Exibição de mensagens via redirecionamento (`RedirectResponse`)
- Rota pública para visualizar o `README.md` via navegador

---

## 🚀 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Uvicorn](https://www.uvicorn.org/) (para rodar o servidor)
- [Markdown](https://python-markdown.github.io/) (para renderizar o README)

---

## 🔐 Sistema de Login

- A rota `/auth/login` permite usuários fazerem login.
- Rotas protegidas exigem autenticação.

### CSRF

- Os formulários possuem proteção contra CSRF usando um token gerado por sessão.

---

## 🛡️ Segurança e Boas Práticas

- A documentação Swagger (`/docs`) pode ser **desativada em produção** para evitar exposição das rotas.
- Sessões são protegidas e os dados armazenados nelas são serializáveis.

---

## 📘 Documentação Personalizada

- Você pode acessar a rota `/readme` para visualizar este arquivo renderizado como HTML.

---


## 🧠 Observações

- Para proteger rotas, você pode criar dependências que verifiquem se o usuário está logado.
- A integração com banco de dados usa SQLAlchemy com sessões gerenciadas por `get_db`.

---

## 📝 Licença

Este projeto está sob a licença [MIT](LICENSE).
