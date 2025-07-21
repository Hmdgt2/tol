// Lista dos anos (ficheiros JSON na pasta dados)
const listaAnos = [
  "2011", "2012", "2013", "2014", "2015",
  "2016", "2017", "2018", "2019", "2020",
  "2021", "2022", "2023", "2024", "2025"
];

// Preenche dropdown 1 a 49
function popularDropdownNumeros() {
  const selectNumero = document.getElementById('numero');
  for (let i = 1; i <= 49; i++) {
    const option = document.createElement('option');
    option.value = i;
    option.textContent = i;
    selectNumero.appendChild(option);
  }
}

// Carrega os dados de um ano
async function carregarDadosAno(ano) {
  const resp = await fetch(`./dados/${ano}.json`);
  if (!resp.ok) throw new Error(`Erro ao carregar dados do ano ${ano}`);
  return await resp.json();
}

// Converte data dd/mm/yyyy para objeto Date para ordenar
function parseData(dataStr) {
  if (!dataStr || typeof dataStr !== 'string') {
    console.warn('dataStr inválido:', dataStr);
    return new Date(0); // ou alguma data padrão, para evitar erro
  }
  const [dia, mes, ano] = dataStr.split('/').map(Number);
  return new Date(ano, mes - 1, dia);
}

// Junta todos os sorteios de todos os anos num array único e ordena por data
async function carregarTodosSorteios() {
  let todosSorteios = [];
  for (const ano of listaAnos) {
    try {
      const dadosAno = await carregarDadosAno(ano);
      todosSorteios = todosSorteios.concat(dadosAno);
    } catch (e) {
      console.warn(e.message);
    }
  }
  todosSorteios.sort((a, b) => parseData(a.data) - parseData(b.data));
  return todosSorteios;
}

function calcularEstatisticas(sorteios, numero) {
  const totalSorteios = sorteios.length;
  let numSaidas = 0;
  let ultimoIndice = -1;

  sorteios.forEach((sorteio, idx) => {
    if (sorteio.numeros.includes(numero)) {
      numSaidas++;
      ultimoIndice = idx;
    }
  });

  const percentSaidas = ((numSaidas / totalSorteios) * 100).toFixed(2);
  const ultimoSorteio = ultimoIndice >= 0 ? sorteios[ultimoIndice].concurso : '-';
  const dataUltimo = ultimoIndice >= 0 ? sorteios[ultimoIndice].data : '-';
  const ausencias = ultimoIndice >= 0 ? totalSorteios - ultimoIndice - 1 : totalSorteios;

  return {
    numero,
    numSaidas,
    percentSaidas,
    ultimoSorteio,
    dataUltimo,
    ausencias,
  };
}

async function main() {
  popularDropdownNumeros();

  document.getElementById('calcularBtn').addEventListener('click', async () => {
    const numero = parseInt(document.getElementById('numero').value, 10);
    if (isNaN(numero) || numero < 1 || numero > 49) {
      alert('Por favor, escolha um número entre 1 e 49');
      return;
    }

    document.getElementById('status').textContent = 'A carregar dados, aguarde...';
    document.getElementById('resultado').style.display = 'none';

    try {
      const sorteios = await carregarTodosSorteios();
      const stats = calcularEstatisticas(sorteios, numero);

      document.getElementById('num').textContent = stats.numero;
      document.getElementById('num_saidas').textContent = stats.numSaidas;
      document.getElementById('percent_saidas').textContent = stats.percentSaidas + '%';
      document.getElementById('ultimo_sorteio').textContent = stats.ultimoSorteio;
      document.getElementById('data_sorteio').textContent = stats.dataUltimo;
      document.getElementById('ausencias').textContent = stats.ausencias;

      document.getElementById('resultado').style.display = 'table';
      document.getElementById('status').textContent = '';
    } catch (err) {
      document.getElementById('status').textContent = 'Erro ao carregar os dados.';
      console.error(err);
    }
  });
}

main();
