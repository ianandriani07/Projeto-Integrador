import React, { useState, useEffect } from 'react';

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

export function ProjectCard({ name, students, coordinators }) {
    if (students === undefined) {
        students = [];
    }

    if (coordinators === undefined) {
        coordinators = [];
    }

    return (
        <div className='project-card'>
            <p>{`Projeto ${name}`}</p>
            <p>{arrayToString('Alunos: ', students)}</p>
            <p>{arrayToString('Coordenadores: ', coordinators)}</p>
            <button>Exibir Dados</button>
            <button>Relatorio</button>
        </div>
    )
}