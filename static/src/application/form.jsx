import "../styles/form.scss";
import React from 'react';
import { createRoot } from 'react-dom/client';

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

function Form() {
    return (<>
        <div className="white rounded-borders-20px card">
            <h1>Test</h1>
        </div>
    </>);
}

const root = document.getElementById('base-form');
const rootElement = createRoot(root);
rootElement.render(<Form />);