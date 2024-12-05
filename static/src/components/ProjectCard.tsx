import "./styles/ProjectCard.scss";
const React = require('react');
const { useState, useEffect } = React;

function arrayToString(prefix, array) {
    let out = prefix;

    if (array.length == 0) {
        return prefix;
    }

    array.forEach(element => {
        out += element + ', ';
    });
    return out.slice(0, -2);
}

export function ProjectCard({ name, students, coordinators, form_ids }: { name: string, students?: Array<string>, coordinators?: Array<string>, form_ids?: Array<string> }) {
    if (students === undefined) {
        students = [];
    }

    if (coordinators === undefined) {
        coordinators = [];
    }

    if (form_ids == undefined) {
        form_ids = [];
    }

    return (
        <div className="project-wrapper">
            <p className="project-name">{`Projeto ${name}`}</p>
            <div className='project-card'>
                <p>{arrayToString('Alunos: ', students)}</p>
                <p>{arrayToString('Coordenadores: ', coordinators)}</p>
                {form_ids.map((id) => {
                    return (
                        <a className="no-style rounded-borders-20px nonsense-white" href={`${id}/form`} >Formulario {id}</a>
                    );
                })}
                <div className="align-in-row pad-top">
                    <a className="no-style rounded-borders-20px cancerous-yellow">Exibir Dados</a>
                    <a className="no-style rounded-borders-20px sad-orange">Relatorio</a>
                </div>
            </div>
        </div>
    )
}