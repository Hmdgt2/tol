let dados = {};
let anoAtual = "2011";
let indiceAtual = 0;

async function carregarDados() {
  const resposta = await fetch(`../dados/${anoAtual}.json`);
  const json = await resposta.json();
  dados = json[anoAtual];
  atualizarInterface();
}

function atualizarInterface() {
  const atual = dados[indiceAtual];
  const proximo = dados[indiceAtual + 1] || {};
  document.getElementById('ano').textContent = anoAtual;
  document.getElementById('concursoAtual').textContent = atual?.concurso || '-';
  document.getElementById('proximoConcurso').textContent = proximo?.concurso || 'Não disponível';
}

function preverProximo() {
  const numeros = new Set();
  while (numeros.size < 2) {
    numeros.add(Math.floor(Math.random() * 49 + 1));
  }
  document.getElementById('previsao').textContent = Array.from(numeros).join(', ');
}

function mostrarResultadoReal() {
  const proximo = dados[indiceAtual + 1];
  if (proximo) {
    document.getElementById('resultadoReal').textContent = proximo.numeros.join(', ');
  } else {
    document.getElementById('resultadoReal').textContent = 'Sem dados do próximo concurso.';
  }
}

function diasEntreDatas(data1, data2) {
  const [d1, m1, a1] = data1.split('/').map(Number);
  const [d2, m2, a2] = data2.split('/').map(Number);
  const date1 = new Date(a1, m1 - 1, d1);
  const date2 = new Date(a2, m2 - 1, d2);
  const diffMs = date2 - date1;
  return diffMs / (1000 * 60 * 60 * 24);
}

async function gerarDesvio() {
  if (indiceAtual + 1 >= dados.length) {
    // Fim do ano, tentar carregar próximo
    const proximoAno = (parseInt(anoAtual) + 1).toString();
    try {
      const resposta = await fetch(`../dados/${proximoAno}.json`);
      if (!resposta.ok) throw new Error("Ficheiro não encontrado");

      const json = await resposta.json();
      const novosDados = json[proximoAno];

      const ultimaData = dados[dados.length - 1].data;
      const primeiraData = novosDados[0]?.data || '00/00/0000';
      const dias = diasEntreDatas(ultimaData, primeiraData);
      if (dias > 21 || dias < 1) {
        console.warn(`⚠️ Diferença anormal entre datas: ${dias} dias (${ultimaData} → ${primeiraData})`);
      }

      // Avança para novo ano
      anoAtual = proximoAno;
      dados = novosDados;
      indiceAtual = 0;
      atualizarInterface();

      document.getElementById('msgDesvio').textContent = `Novo ano (${anoAtual}) carregado. Pronto para continuar.`;
    } catch (e) {
      document.getElementById('msgDesvio').textContent = `Fim da simulação. Não foi possível carregar o ano ${proximoAno}.`;
    }
    return;
  }

  const previsao = document.getElementById('previsao').textContent.split(', ').map(Number);
  const proximo = dados[indiceAtual + 1];

  if (!previsao.length || !proximo) return;

  const acertos = previsao.filter(n => proximo.numeros.includes(n));
  const desvio = {
    concurso: proximo.concurso,
    data: proximo.data,
    previsao,
    resultado: proximo.numeros,
    acertos: acertos.length,
    numerosCertos: acertos
  };

  console.log('Gerado JSON de desvio:', desvio);
  document.getElementById('msgDesvio').textContent = 'Desvio gerado! Consulte consola para verificar.';

  indiceAtual++;
  atualizarInterface();
  document.getElementById('previsao').textContent = '';
  document.getElementById('resultadoReal').textContent = '';
  document.getElementById('msgDesvio').textContent += ' Pronto para o próximo concurso.';
}

carregarDados();
