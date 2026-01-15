🧠🏁 AC-ML-Race-Engineer

Machine Learning Race Engineer for Assetto Corsa

AC-ML-Race-Engineer é um sistema de telemetria em tempo real, big-data e machine learning projetado especificamente para o Assetto Corsa. Ele captura cada volta, constrói datasets personalizados por pista + carro, treina modelos de ML e fornece coaching ao vivo enquanto você pilota.

Diferente de ferramentas de telemetria comuns, esta é uma plataforma de modelagem de piloto e engenharia de corrida.

🚀 Funcionalidades

Captura de Telemetria Raw: Extração direta via shared memory do Assetto Corsa.

Big Data Automático: Armazena voltas em arquivos CSV organizados por pista e veículo.

Log Abrangente:

Velocidade, acelerador, freio, direção (steering).

Temperaturas, desgaste e slip dos pneus.

Temperatura de freios, atuação de ABS e TC.

Forças G, aderência (grip) e temperatura da pista.

Modelos de ML Dedicados: Treina um "cérebro" específico para cada combinação de pista/carro.

Predições em Tempo Real:

Velocidade alvo (target speed).

Delta de performance vs. sua melhor versão.

Feedback ao Vivo: Coaching visual/técnico durante a pilotagem.

WebSocket API: Expõe dados processados para dashboards externos e apps móveis.

🧬 Conceito Central

Cada Pista + Carro possui seu próprio modelo de ML único. O sistema aprende:

"Como VOCÊ pilota ESTE carro nesta pista específica."

Isso permite:

Comparação justa de ritmo.

Coaching personalizado.

Sistemas de Race Control inteligentes.

Futuros "Steward AIs" para análise de incidentes.

📁 Estrutura do Projeto
code
Text
download
content_copy
expand_less
AC-ML-Race-Engineer/
├── main.py              # Telemetria ao vivo + WebSocket + Feedback ML
├── ideal_engine.py      # Logger de telemetria + Builder de datasets
├── engineer_ai.py       # Engine de inferência do ML
├── train_model.py       # Script para treino offline dos modelos
├── ac_reader.py         # Leitor de Shared Memory do Assetto Corsa
└── ac_structs.py        # Estruturas de memória do AC (C++ structs)
📂 Organização de Dados & Modelos

O sistema organiza automaticamente os dados seguindo a hierarquia:

Dados (CSVs)

data/monza/ks_porsche_911_gt3_cup_2017/lap_20260115_012233.csv

Modelos (Pickle)

models/monza/ks_porsche_911_gt3_cup_2017/ia_engineer.pkl

🖥️ Instalação
Pré-requisitos

Python 3.10 ou superior

Assetto Corsa (PC)

Content Manager (recomendado)

Dependências

Instale as bibliotecas necessárias via pip:

code
Bash
download
content_copy
expand_less
pip install numpy pandas scikit-learn joblib websockets
▶️ Como Usar

Inicie o sistema:

code
Bash
download
content_copy
expand_less
python main.py

Vá para a pista: Abra o Assetto Corsa e comece a dirigir. A telemetria será gravada automaticamente.

Treine a IA: Após algumas voltas rápidas, encerre o main.py e execute:

code
Bash
download
content_copy
expand_less
python train_model.py

Isso carregará todos os CSVs coletados e gerará o arquivo ia_engineer.pkl.

Coaching em tempo real: Na próxima vez que você rodar o main.py e for para a pista, o modelo de ML será carregado e fornecerá feedback ao vivo.

🔌 WebSocket API

O servidor roda por padrão em: ws://127.0.0.1:8765

Você pode consumir os dados em tempo real para criar overlays ou apps. Exemplo de output JSON:

code
JSON
download
content_copy
expand_less
{
  "rpm": 7420,
  "speed": 186.3,
  "target_speed": 191.4,
  "delta_speed": -5.1
}
🧪 Status do Projeto

Este é um projeto experimental de pesquisa em engenharia e ML para sim racing.

⚠️ Não é um produto finalizado.

⚠️ Não é um cheat ou trapaça.

⚠️ Não é um piloto automático.

Foco: Análise de dados, coaching assistido por IA e pesquisa de comportamento de piloto.

🧠 Visão de Futuro

Tornar-se o primeiro sistema de engenharia de corrida e controle de prova (Race Control) totalmente baseado em Machine Learning para o ecossistema de simulação.

📜 Licença

Distribuído sob a licença MIT. Veja LICENSE para mais informações.