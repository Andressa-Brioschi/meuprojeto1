// Etapas do cadastro
let stepAtual = 0;
const steps = document.querySelectorAll(".step");

function showStep(index) {
  steps.forEach((step, i) => {
    step.style.display = i === index ? "flex" : "none";
  });
}

function nextStep() {
  if (stepAtual < steps.length - 1) {
    stepAtual++;
    showStep(stepAtual);
  }
}

function prevStep() {
  if (stepAtual > 0) {
    stepAtual--;
    showStep(stepAtual);
  }
}

showStep(stepAtual);

// Validação das senhas

document.getElementById ("btn_dispose").addEventListener ("click", disposeDiv, false);
div_erro = document.getElementById("erro_div")

function disposeDiv(){
    div_erro.style.display = 'none';
}