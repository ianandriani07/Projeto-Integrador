import "../styles/form.scss";
const React = require('react');
const { createRoot } = require('react-dom/client');
import { Header } from "../components/Header.tsx";

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

function TextQuestion({ text }: { text: string }) {
    return (
        <div className="card">
            <p>{text}</p>
            <input></input>
        </div>
    );
}

function NumericQuestion({ text }: { text: string }) {
    return (
        <div className="card">
            <p>{text}</p>
            <input type="number"></input>
        </div>
    );
}

function Formula({ text }: { text: string }) {
    return (
        <div className="card force-shorter">
            <p>{text} Output Aqui</p>
        </div>
    );
}

function Form() {
    return (<>
        <Header />
        <div className="questions-field align-in-column">
            <TextQuestion text="Nome:"></TextQuestion>
            <NumericQuestion text="Idade:"></NumericQuestion>
            <Formula text="Formula:"></Formula>
        </div>
    </>);
}

const root = document.getElementById('base-form');
const rootElement = createRoot(root);
rootElement.render(<Form />);