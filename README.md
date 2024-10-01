# Tec-Help
Tec Help - Sistema Simples para Gerenciamento de Tickets de Chamados/ Simple Program for Tech Support Ticket Management

O TEC HELP é um sistema desenvolvido com o propósito de ajudar profissionais de suporte em TI a gerenciarem seus chamados de forma simples e direta, sem pagar absurdos por um sistema de ticket bloatado, nem ter que lidar com um alto volume de chamados de forma desorganizada, podendo assim gerar relatórios concisos a respeito da produtividade da equipe.
A metodologia deste programa é bastante simples (simplório, eu diria), de forma que o técnico irá copiar os códigos-fonte para um computador que servirá como servidor, admitindo acesso pelas máquinas-cliente via compartilhamento de pasta (SMB) e em seguida, criar um atalho de acesso ao código "1login.py", que será acessado diretamente pelo usuário. Toda a hierarquia de acessos é baseada em login. Há os usuários comuns e os administradores. O usuário padrão acessa diretamente a área de abertura de chamados. O administrador acessa diretamente a área de suporte técnico. Deve ser criado um banco de dados PostgreSQL, em qualquer máquina que tenha suporte para o acesso concomitante de muitos usuários, a depender de cada contexto. As credenciais de acesso ao banco de dados estão localizadas direto no início de cada arquivo .py , hard-codadas no código fonte (disse que o sistema era simplório, sinta-se à vontade para melhorá-lo). No arquivo "criabanco.py", você poderá acessar quais tabelas serão criadas, lembre-se de instalar o PostgreSQL no seu servidor antes de rodar o script.

Recomendamos o uso da versão 3.12.4 do Python para ambientes 64-bits e a versão 3.8.6 para ambientes 32-bits. O Python deve ser instalado em todas as máquinas cliente.

Instale os seguintes bibliotecas via pip: psycopg2, datetime, image, pandas, requests.



TEC HELP is a system designed to help IT support professionals manage their tickets in a simple and straightforward way, without paying absurd amounts for a bloated ticketing system or having to deal with a high volume of tickets in a disorganized way, thus being able to generate concise reports on the team's productivity.
The methodology of this program is quite simple (simplistic, I would say), so the technician will copy the source code to a computer that will serve as a server, allowing access by client machines via folder sharing (SMB) and then create a shortcut to access the code “1login.py”, which will be accessed directly by the user. The entire access hierarchy is based on login. There are standard users and administrators. The standard user accesses the ticket opening area directly. The administrator accesses the technical support area directly. A PostgreSQL database must be created on any machine that supports concurrent access by many users, depending on each context. The credentials for accessing the database are located directly in every .py file, hard-coded into the source code (I said the system was simple, feel free to improve it). In the “criabanco.py” file, you can access which tables will be created. Remember to install PostgreSQL on your server before running the script.

We recommend using Python version 3.12.4 for 64-bit environments and version 3.8.6 for 32-bit environments. Python must be installed on all client machines.

Install the following libraries via pip: psycopg2, datetime, image, pandas, requests.

