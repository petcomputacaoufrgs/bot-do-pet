# Bot para Discord

#### Projeto: Atividade Internas

#### Linguagem utilizada: Python (versão 3.10.6)

##### Autores: [Ian](https://github.com/kerszamaral), [Nathan](https://github.com/neitaans) e [Vic](https://github.com/vickyad)

## Descrição

Bot do Discord com diversas funcionalidades para ajudar no dia a dia dos bolsistas, contribuir com o aprendizado de Python e da biblioteca `discord.py` e funcionalidades divertidas para integração e descontração

## Como instalar e rodar:
### Entre na pasta clonada do repositorio e utilize os seguintes comandos:

### Para utilizar o codigo de forma limpa, crie um venv com 
```
python3 -m venv <pastadoprojeto>
```
### Após isso, rode o seguinte comando para ativar o ambiente de trabalho
```
source <pastadoprojeto>/bin/activate
```

### Para instalar todas as dependencias, rode
```
pip install -r requirements.txt
```

### Por fim, é possivel rodar o bot com
```
python3 -m main
```

## Comandos disponíveis

> prefixo: `pet.`

### Help

Mostra todos os comandos possíveis

#### Uso

```
pet.help
```

---

### Xingar o Matheus

Não é necessário gastar sua saliva xingando o Matheus, o bot faz isso por você

#### Uso

```
pet.xingar_matheus
```

---

### Adionar xingamento

Adicione uma nova forma de ofender o Matheus!

#### Uso

```
pet.add_xingamento <xingamento goes here>
```

---

### Remover xingamento

Não gostou de algum xingamento? Ele nunca mais será usado

#### Uso

```
pet.rem_xingamento <xingamento goes here>
```

---

### Listar xingamentos

Lista todas as formas possíveis de ofender o Matheus

#### Uso

```
pet.xingamentos
```

---

### Elogiar

Elogie alguém que fez um bom trabalho recentemente!

#### Uso

```
pet.elogiar @someone
```

---

### Adicionar elogio

Adicione mais uma forma de reconhecermos o bom trabalho dos nossos coleguinhas

#### Uso

```
pet.add_elogio <elogio goes here>
```

---

### Remover elogio

Não gostou de algum elogio? Não usaremos mais

#### Uso

```
pet.rem_elogio <elogio goes here>
```

---

### Listar elogios

Lista todas as formas de elogiar os outros

#### Uso

```
pet.elogios
```

---

### Abraçar

Demonstre seu carinho por alguém

#### Uso

```
pet.hug @someone
```

---

### Mostrar próxima retrospectiva

Avisa quantos dias faltam pra retrospectiva

#### Uso

```
pet.retro
```

---

### Settar a próxima retrospectiva

Seta a nova data para a retrospectiva, no formato _dd/mm_

#### Uso

```
pet.retro_manual <dia/mes>
```

---

### Férias da retrospectiva

Desliga os avisos de retrospectiva

#### Uso

```
pet.retro_ferias
```

---

### Mostrar próximo interpet

Avisa quantos dias faltam pra interpet

#### Uso

```
pet.inter
```

---

### Settar a próximo interpet

Seta a nova data para a interpet, no formato _dd/mm_

#### Uso

```
pet.inter_manual <dia/mes>
```

---

### Férias do interpet

Desliga os avisos de interpet

#### Uso

```
pet.inter_ferias
```

---

### Liderança

Saiba quem manda no PET nesse mês

#### Uso

```
pet.lideres
```

---

### Aviso

Use para criar um aviso 100% personalizável

#### Uso

```
1ª chamada: pet.aviso
2ª chamada: pet.aviso <nome do aviso>
3ª chamada: pet.aviso <tempo até o aviso acontecer> ou <dd/mm/aaaa>
4ª chamada: pet.aviso <@pessoa 1> <@pessoa 2> ... <@pessoa n>
5ª chamada: pet.aviso <#nome do canal>
```

---

### Aviso atual

Use para checar se há um aviso já criado e, caso haja, use para obter um resumo sobre ele.

#### Uso

```
pet.aviso_atual
```

---

## Melhorias a serem feitas
- Melhoria na verificação de entradas no evento
- Fazer com que seja possível haver diversos eventos ao mesmo tempo sem interferência
