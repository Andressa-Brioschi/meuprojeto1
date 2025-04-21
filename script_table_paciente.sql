create database projeto_semestral;
use projeto_semestral;
create table cadastro_paciente(
nome varchar(200) not null,
cpf char(11) primary key,
data_nasc date not null,
email varchar (100) not null,
senha varchar(200) not null,
telefone char(11) not null,
cep char(8) not null,
rua varchar(200) null,
bairro varchar(200) null,
cidade varchar(200) null,
UF char(2) not null );






