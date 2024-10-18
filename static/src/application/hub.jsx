import "../styles/hub.scss";
import React from 'react';
import { createRoot } from 'react-dom/client';
import { IconButton } from '../components/IconButton.jsx'
import { ProjectCard } from '../components/ProjectCard.jsx'

function Hub() {
    return (
        <>
            <button className="no-style logout-button" iconPath={'no.png'}><span>&#10005;</span>Logout</button>
            <div className="align-in-row-left">
                <img className="logo" src="/static/icons/backbone.png" />
                <h1 className="title">Bem Vindo “Usuario”</h1>
            </div>
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