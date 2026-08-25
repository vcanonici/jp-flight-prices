# Japan Flight Prices

Histórico diário de preços de voos de Portugal para o Japão, pesquisado e atualizado pelo ChatGPT.

## Rotas monitoradas

- LIS → Tóquio (TYO / HND / NRT)
- OPO → Tóquio (TYO / HND / NRT)
- LIS → Osaka (OSA / KIX)
- OPO → Osaka (OSA / KIX)

## Dados

Os resultados ficam em `data/flight_prices.csv`.

Cada linha representa o menor preço comparável encontrado para uma rota em uma execução diária. Tarifas aéreas mudam rapidamente e podem expirar entre a coleta e a compra.

## Automação

A coleta é executada por uma tarefa agendada do ChatGPT. Após cada coleta, o ChatGPT atualiza o CSV e faz commit no `main`.

A pipeline do GitHub Actions valida o schema e a integridade básica do dataset em pushes e pull requests. Outra Action regenera automaticamente a tabela abaixo sempre que o CSV muda.

<!-- PRICE_HISTORY_START -->
## Histórico de preços

Menor tarifa de ida e volta encontrada em cada execução diária.

| Dia | LIS → Tóquio | OPO → Tóquio | LIS → Osaka | OPO → Osaka |
|---|---:|---:|---:|---:|
| 2026-08-25 | €882 | €737 | €730 | €728 |

_Gerado automaticamente a partir de `data/flight_prices.csv`._
<!-- PRICE_HISTORY_END -->
