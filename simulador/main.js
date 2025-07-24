let dados = {};
let anoAtual = "2011";
let indiceAtual = 0;

// Referências aos botões (devem existir no simulador.html)
const btnPrever = document.querySelector('button[onclick="preverProximo()"]');
const btnMostrar = document.querySelector('button[onclick="mostrarResultadoReal()"]');
const btnGerar = document.querySelector('button[onclick="gerarDesvio()"]');
const btnAtualizar = document.getElementById('btnAtualizar'); // botão novo que vais criar

// Função para ativar/desativar botões conforme o estado da simulação
function setBotoesEstado(prever, mostrar, gerar, atualizar) {
  btnPrever.disabled = !prever;
  btnMostrar.disabled = !mostrar;
  btnGerar.disabled = !gerar;

  if (atualizar) {
    btnAtualizar.classList.remove('hidden');
  } else {
    btnAtualizar.classList.add('hidden');
  }
}

async function carregarDados() {
  const resposta = await fetch(`../dados/${anoAtual}.json`);
  const json = await resposta.json();
  dados = json[anoAtual];
  indiceAtual = 0; // garantir começa no primeiro concurso do ano
  atualizarInterface();
}

function atualizarInterface() {
  const atual = dados[indiceAtual];
  const proximo = dados[indiceAtual + 1] || {};

  document.getElementById('ano').textContent = anoAtual;
  document.getElementById('concursoAtual').textContent = atual?.concurso || '-';
  document.getElementById('proximoConcurso').textContent = proximo?.concurso || 'Não disponível';

  // Limpar previsao, resultado e mensagens
  document.getElementById('previsao').textContent = '';
  document.getElementById('resultadoReal').textContent = '';
  document.getElementById('msgDesvio').textContent = '';

  // Estado inicial: só o botão "Prever" ativo
  setBotoesEstado(true, false, false, false);
}

function preverProximo() {
  const numeros = new Set();
  while (numeros.size < 2) {
    numeros.add(Math.floor(Math.random() * 49 + 1));
  }
  document.getElementById('previsao').textContent = Array.from(numeros).join(', ');

  // Desativa Prever, ativa Mostrar Resultado
  setBotoesEstado(false, true, false, false);
}

function mostrarResultadoReal() {
  const proximo = dados[indiceAtual + 1];
  if (proximo) {
    document.getElementById('resultadoReal').textContent = proximo.numeros.join(', ');
  } else {
    document.getElementById('resultadoReal').textContent = 'Sem dados do próximo concurso.';
  }

  // Desativa Mostrar Resultado, ativa Gerar JSON
  setBotoesEstado(false, false, true, false);
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

  // Desativa gerar e ativa botão atualizar
  setBotoesEstado(false, false, false, true);
}

// Função chamada pelo botão "Atualizar Simulação"
async function atualizarSimulacao() {
  indiceAtual++;

  if (indiceAtual + 1 >= dados.length) {
    // Fim do ano, tentar carregar próximo
    const proximoAno = (parseInt(anoAtual) + 1).toString();
    try {
      const resposta = await fetch(`../dados/${proximoAno}.json`);
      if (!resposta.ok) throw new Error("Ficheiro não encontrado");

      const json = await resposta.json();
      const novosDados = json[proximoAno];

      // Verificar diferença de datas
      const ultimaData = dados[dados.length - 1].data;
      const primeiraData = novosDados[0]?.data || '00/00/0000';
      const dias = diasEntreDatas(ultimaData, primeiraData);
      if (dias > 21 || dias < 1) {
        console.warn(`⚠️ Diferença anormal entre datas: ${dias} dias (${ultimaData} → ${primeiraData})`);
      }

      // Troca ano e dados
      anoAtual = proximoAno;
      dados = novosDados;
      indiceAtual = 0;

    } catch (e) {
      document.getElementById('msgDesvio').textContent = `Fim da simulação. Não foi possível carregar o ano ${proximoAno}.`;
      setBotoesEstado(false, false, false, false);
      return;
    }
  }

  atualizarInterface();
}

carregarDados();
