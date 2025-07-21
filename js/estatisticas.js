const fs = require('fs');
const path = require('path');

// Pasta dados e estatisticas uma nível acima de 'js'
const PASTA_DADOS = path.join(__dirname, '..', 'dados');
const PASTA_ESTATISTICAS = path.join(__dirname, '..', 'estatisticas');

// Função para parsear data no formato "dd/mm/yyyy"
function parseData(dataStr) {
  const partes = dataStr.split('/');
  if (partes.length !== 3) return new Date(0);
  const [dia, mes, ano] = partes.map(Number);
  return new Date(ano, mes - 1, dia);
}

// Lista os ficheiros JSON na pasta dados que correspondem a anos (2011-2025)
function listarFicheirosAnos() {
  const files = fs.readdirSync(PASTA_DADOS);
  return files.filter(f => {
    const ano = f.replace('.json', '');
    return /^\d{4}$/.test(ano) && Number(ano) >= 2011 && Number(ano) <= 2025;
  });
}

// Lê os sorteios de um ficheiro JSON específico
function lerSorteiosAno(nomeFicheiro) {
  const caminho = path.join(PASTA_DADOS, nomeFicheiro);
  const conteudo = fs.readFileSync(caminho, 'utf-8');
  const dados = JSON.parse(conteudo);
  const ano = nomeFicheiro.replace('.json', '');
  return dados[ano] || [];
}

// Carrega e junta todos os sorteios dos ficheiros da pasta
function carregarTodosSorteios() {
  const ficheiros = listarFicheirosAnos();
  let todos = [];
  ficheiros.forEach(fich => {
    try {
      const sorteios = lerSorteiosAno(fich);
      todos = todos.concat(sorteios);
    } catch (e) {
      console.warn(`[Aviso] Erro a ler ${fich}:`, e.message);
    }
  });
  // Ordena por data
  todos.sort((a, b) => parseData(a.data) - parseData(b.data));
  return todos;
}

// Calcula estatísticas para números de 1 a 49
function calcularEstatisticas(sorteios) {
  const total = sorteios.length;
  const estatisticas = {};

  for (let numero = 1; numero <= 49; numero++) {
    let num_saidas = 0;
    let ultimo_idx = -1;

    sorteios.forEach((sorteio, idx) => {
      if (sorteio.numeros && sorteio.numeros.includes(numero)) {
        num_saidas++;
        ultimo_idx = idx;
      }
    });

    const percent = total ? Number(((num_saidas / total) * 100).toFixed(2)) : 0;

    let ultimo_sorteio = "-";
    let data_ultimo = "-";
    let ausencias = total;

    if (ultimo_idx >= 0) {
      ultimo_sorteio = sorteios[ultimo_idx].concurso || "-";
      data_ultimo = sorteios[ultimo_idx].data || "-";
      ausencias = total - ultimo_idx - 1;
    }

    estatisticas[numero.toString()] = {
      numero,
      num_saidas,
      percent_saidas: percent,
      ultimo_sorteio,
      data_ultimo,
      ausencias
    };
  }

  return estatisticas;
}

// Cria pasta se não existir
function garantirPasta(pasta) {
  if (!fs.existsSync(pasta)) {
    fs.mkdirSync(pasta, { recursive: true });
  }
}

// Função principal
function main() {
  console.log("A carregar sorteios...");
  const sorteios = carregarTodosSorteios();
  console.log(`Foram carregados ${sorteios.length} sorteios.`);

  console.log("A calcular estatísticas...");
  const estatisticas = calcularEstatisticas(sorteios);

  const resultado = {
    total_sorteios: sorteios.length,
    estatisticas_por_numero: estatisticas
  };

  garantirPasta(PASTA_ESTATISTICAS);

  const destino = path.join(PASTA_ESTATISTICAS, 'estatisticas_stacasa.json');

  fs.writeFileSync(destino, JSON.stringify(resultado, null, 2), 'utf-8');

  console.log(`Estatísticas guardadas em: ${destino}`);
}

main();
