import "../styles/hub.scss";
const React = require('react');
const { createRoot } = require('react-dom/client');
import { IconButton } from '../components/IconButton.tsx';
import { ProjectCard } from '../components/ProjectCard.tsx';
import { Header } from "../components/Header.tsx";

function Hub() {
    return (
        <>
            <Header title='Bem Vindo “Usuario”' logout={true} />
            <nav>
                <IconButton className="no-style hub-icon-button" iconPath={"/static/icons/torso.svg"}>Adicionar Usuario</IconButton>
                <IconButton className="no-style hub-icon-button" iconPath={"/static/icons/plus.svg"}>Adicionar Projeto</IconButton>
                <IconButton className="no-style hub-icon-button" iconPath={"/static/icons/pencil.svg"}>Adicionar Formulario</IconButton>
                <IconButton className="no-style hub-icon-button" iconPath={"/static/icons/cog.svg"}>Configurações</IconButton>
            </nav>
            <div className="card-holder">
                <ProjectCard name={"Test"} students={['Fabio', 'Augusto', 'Jorjão Berranteiro']} coordinators={['Sua mãe']} />
            </div>
        </>
    )
};

const root = document.getElementById('base-hub');
const rootElement = createRoot(root);
rootElement.render(<Hub />);