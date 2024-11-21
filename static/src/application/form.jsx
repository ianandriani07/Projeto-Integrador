require("../styles/form.scss");
const React = require('react');
const { createRoot } = require('react-dom/client');

let test = [
    {
        "id": 0,
        "texto": "Escreva seu endereço",
        "tipo": "Textual",
        "variavel_associacao": "endereco"
    },
    {
        "id": 1,
        "texto": "Qual das opções é melhor?",
        "tipo": "Multipla Escolha",
        "variavel_associacao": "endereco"
    }
];

function TextQuestion() {

}

function Form() {
    return (<>
        <div className="background-white rounded-borders-20px card">
            <h1>Test</h1>
        </div>
    </>);
}

const root = document.getElementById('base-form');
const rootElement = createRoot(root);
rootElement.render(<Form />);