// estatisticas.js

let dadosAnos = null;

async function carregarDados(dadosURL) {
  const resp = await fetch(dadosURL);
  if (!resp.ok) throw new Error('Erro ao carregar ficheiro JSON.');
  dadosAnos = await resp.json();
}

function popularDropdownAnos() {
  const selectAno = document.getElementById('ano');
  selectAno.innerHTML = '';
  const anos = Object.keys(dadosAnos).sort();
  for (const ano of anos) {
    const option = document.createElement('option');
    option.value = ano;
    option.textContent = ano;
    selectAno.appendChild(option);
  }
}

function calcularEstatisticas(dados, numero) {
  const totalSorteios = dados.length;
  let numSaidas = 0;
  let ultimoSorteio = null;
  let dataUltimo = null;
  let ultimoIndice = -1;

  dados.forEach((sorteio, idx) => {
    if (sorteio.numeros.includes(numero)) {
      numSaidas++;
      ultimoSorteio = sorteio.concurso;
      dataUltimo = sorteio.data;
      ultimoIndice = idx;
    }
  });

  const ausencias = ultimoIndice >= 0 ? totalSorteios - ultimoIndice - 1 : totalSorteios;
  const percentSaidas = ((numSaidas / totalSorteios) * 100).toFixed(2);

  return {
    numero,
    numSaidas,
    percentSaidas,
    ultimoSorteio: ultimoSorteio || '-',
    dataUltimo: dataUltimo || '-',
    ausencias,
  };
}

function inicializar(dadosURL) {
  carregarDados(dadosURL)
    .then(() => {
      popularDropdownAnos();
      document.getElementById('status').textContent = 'Dados carregados. Escolha o ano e número.';
    })
    .catch(err => {
      document.getElementById('status').textContent = 'Erro ao carregar os dados.';
      console.error(err);
    });

  document.getElementById('calcularBtn').addEventListener('click', () => {
    const numero = parseInt(document.getElementById('numero').value, 10);
    const ano = document.getElementById('ano').value;

    if (isNaN(numero) || numero < 1 || numero > 50) {
      alert('Por favor, insira um número entre 1 e 50.');
      return;
    }
    if (!ano || !(ano in dadosAnos)) {
      alert('Por favor, selecione um ano válido.');
      return;
    }

    const dadosAno = dadosAnos[ano];
    const stats = calcularEstatisticas(dadosAno, numero);

    document.getElementById('num').textContent = stats.numero;
    document.getElementById('num_saidas').textContent = stats.numSaidas;
    document.getElementById('percent_saidas').textContent = stats.percentSaidas + '%';
    document.getElementById('ultimo_sorteio').textContent = stats.ultimoSorteio;
    document.getElementById('data_sorteio').textContent = stats.dataUltimo;
    document.getElementById('ausencias').textContent = stats.ausencias;

    document.getElementById('resultado').style.display = 'table';
    document.getElementById('status').textContent = '';
  });
}
