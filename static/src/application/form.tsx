import "../styles/form.scss";
import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Header } from "../components/Header.tsx";
import { Processor, DefaultFunctions } from "../js/processor.ts";

interface ProcessorFunctions {
	addVariable: (varName: string, value: any, aliasValue?: string) => void,
	addTable: (table: Object, alias?: string) => void,
	execute: (formula: string) => number,
}

enum QuestionType {
	SingleCategoricalQuestion = 'objetva',
	Formula = "formula",
}

interface Option {
	id: number,
	ordem: number,
	pontuacao: number,
	texto: string
}

interface SingleCategoryQuestionType {
	id: number,
	varName: string,
	text: string,
	necessary: boolean,
	options: Array<Option>,
	conversionTable: Object,
	processor: ProcessorFunctions
}

interface FormulaQuestionType {
	text: string,
	formula: string,
	process: ProcessorFunctions
}

interface SingleCategoricalQuestionJSON {
	id: number,
	id_formulario: number,
	nome_variavel: string,
	obrigatoria: boolean,
	opcoes: Array<Option>,
	ordem: number,
	tabela_conversao: Object,
	texto: string,
	tipo: QuestionType
}

interface FormulaQuestionJSON {
	texto: string,
	formula: string,
	tipo: QuestionType
}

interface FormJSON {
	id_formulario: number,
	pagina_atual: number,
	total_paginas: number,
	total_registros: number,
	perguntas: Array<SingleCategoricalQuestionJSON | FormulaQuestionJSON>
}

interface RenderJSON {
	json: FormJSON,
	processor: ProcessorFunctions
}

let test = {
	"perguntas": [
		{
			"id": 4,
			"id_formulario": 1,
			"nome_variavel": "forca",
			"obrigatoria": false,
			"opcoes": [
				{
					"id": 7,
					"ordem": 1,
					"pontuacao": 0,
					"texto": "Nenhuma"
				},
				{
					"id": 8,
					"ordem": 2,
					"pontuacao": 1,
					"texto": "Alguma"
				},
				{
					"id": 9,
					"ordem": 3,
					"pontuacao": 2,
					"texto": "Muita ou não consegue"
				}
			],
			"ordem": 1,
			"tabela_conversao": {
				"Alguma": 1,
				"Muita ou não consegue": 2,
				"Nenhuma": 0
			},
			"texto": "O quanto de dificuldade você tem para levantar e carregar 5kg?",
			"tipo": "objetiva"
		},
		{
			"id": 5,
			"id_formulario": 1,
			"nome_variavel": "ajuda_caminhar",
			"obrigatoria": false,
			"opcoes": [
				{
					"id": 10,
					"ordem": 1,
					"pontuacao": 0,
					"texto": "Nenhuma"
				},
				{
					"id": 11,
					"ordem": 2,
					"pontuacao": 1,
					"texto": "Alguma"
				},
				{
					"id": 12,
					"ordem": 3,
					"pontuacao": 2,
					"texto": "Muita, usa apoios ou é incapaz"
				}
			],
			"ordem": 2,
			"tabela_conversao": {
				"Alguma": 1,
				"Muita, usa apoios ou é incapaz": 2,
				"Nenhuma": 0
			},
			"texto": "O quanto de dificuldade você tem para atravessar um cômodo?",
			"tipo": "objetiva"
		},
		{
			"id": 6,
			"id_formulario": 1,
			"nome_variavel": "levantar_cadeira",
			"obrigatoria": false,
			"opcoes": [
				{
					"id": 13,
					"ordem": 1,
					"pontuacao": 0,
					"texto": "Nenhuma"
				},
				{
					"id": 14,
					"ordem": 2,
					"pontuacao": 1,
					"texto": "Alguma"
				},
				{
					"id": 15,
					"ordem": 3,
					"pontuacao": 2,
					"texto": "Muita ou não consegue sem ajuda"
				}
			],
			"ordem": 3,
			"tabela_conversao": {
				"Alguma": 1,
				"Muita ou não consegue sem ajuda": 2,
				"Nenhuma": 0
			},
			"texto": "O quanto de dificuldade você tem para levantar de uma cama ou cadeira?",
			"tipo": "objetiva"
		},
		{
			"id": 7,
			"id_formulario": 1,
			"nome_variavel": "subir_escadas",
			"obrigatoria": false,
			"opcoes": [
				{
					"id": 16,
					"ordem": 1,
					"pontuacao": 0,
					"texto": "Nenhuma"
				},
				{
					"id": 17,
					"ordem": 2,
					"pontuacao": 1,
					"texto": "Alguma"
				},
				{
					"id": 18,
					"ordem": 3,
					"pontuacao": 2,
					"texto": "Muita ou não consegue"
				}
			],
			"ordem": 4,
			"tabela_conversao": {
				"Alguma": 1,
				"Muita ou não consegue": 2,
				"Nenhuma": 0
			},
			"texto": "O quanto de dificuldade você tem para subir um lance de escadas de 10 degraus?",
			"tipo": "objetiva"
		},
		{
			"id": 8,
			"id_formulario": 1,
			"nome_variavel": "quedas",
			"obrigatoria": false,
			"opcoes": [
				{
					"id": 19,
					"ordem": 1,
					"pontuacao": 0,
					"texto": "Nenhuma"
				},
				{
					"id": 20,
					"ordem": 2,
					"pontuacao": 1,
					"texto": "1-3 quedas"
				},
				{
					"id": 21,
					"ordem": 3,
					"pontuacao": 2,
					"texto": "4 ou mais quedas"
				}
			],
			"ordem": 5,
			"tabela_conversao": {
				"1-3 quedas": 1,
				"4 ou mais quedas": 2,
				"Nenhuma": 0
			},
			"texto": "Quantas vezes você caiu no último ano?",
			"tipo": "objetiva"
		},
		{
			"id": 9,
			"id_formulario": 1,
			"nome_variavel": "cp",
			"obrigatoria": false,
			"opcoes": [
				{
					"id": 22,
					"ordem": 1,
					"pontuacao": 0,
					"texto": " Mulher e CP > 33cm"
				},
				{
					"id": 23,
					"ordem": 2,
					"pontuacao": 10,
					"texto": "Mulher e CP <= 33cm"
				},
				{
					"id": 24,
					"ordem": 3,
					"pontuacao": 0,
					"texto": "Homens e CP > 34cm"
				},
				{
					"id": 25,
					"ordem": 4,
					"pontuacao": 10,
					"texto": "Homens e CP <= 34cm"
				}
			],
			"ordem": 6,
			"tabela_conversao": {
				" Mulher e CP > 33cm": 0,
				"Homens e CP <= 34cm": 10,
				"Homens e CP > 34cm": 0,
				"Mulher e CP <= 33cm": 10
			},
			"texto": "Qual valor da Circunferência da Panturrilha?",
			"tipo": "objetiva"
		},
		{
			"texto": "Resultado",
			"formula": "forca + ajuda_caminhar + levantar_cadeira + subir_escadas + quedas + cp >= 11",
			"tipo": "formula"
		}
	],
};

function JSONRender({ json, processor }: RenderJSON) {
	let rendered: Array<Element> = [];
	let id = 0;

	json.perguntas.forEach((question) => {
		switch (question.tipo) {
			case 'objetiva' as QuestionType:
				{
					const q = question as SingleCategoricalQuestionJSON;
					rendered.push((
						<SingleCategoricalQuestion id={id} necessary={q.obrigatoria}
							options={q.opcoes} processor={processor} text={question.texto}
							varName={q.nome_variavel} conversionTable={q.tabela_conversao} />
					));
					id += q.opcoes.length;
				}
				break;
			case "formula" as QuestionType:
				{
					let q = question as FormulaQuestionJSON;
					rendered.push(
						(
							<FormulaQuestion text={q.texto} formula={q.formula} process={processor} />
						)
					);
				}
				break;
		}
	});

	return (
		<>
			{rendered}
		</>
	);
}

function TextQuestion({ text }: { text: string }) {
	return (
		<div className="card">
			<p>{text}</p>
			<input className="writable-field"></input>
		</div>
	);
}

function NumericQuestion({ text }: { text: string }) {
	return (
		<div className="card">
			<p>{text}</p>
			<input className="writable-field" type="number"></input>
		</div>
	);
}

function SingleCategoricalQuestion({ id, varName, text, necessary, options, conversionTable, processor }: SingleCategoryQuestionType): Element {

	let optionsEl: Array<Element> = [];
	let [idChecked, setIdChecked] = useState(id);

	processor.addTable(conversionTable, varName);

	options.forEach((op, i) => {
		optionsEl.push(
			(
				<div key={i}>
					<input id={varName + (id + i).toString()} type="radio" onChange={() => { setIdChecked(id + i); processor.addVariable(varName, op.texto, varName) }} checked={idChecked == (id + i)}></input>
					<label htmlFor={varName + (id + i).toString()}>{op.texto}</label>
				</div >
			)
		);
	});

	return (
		<div className="card">
			<p>{text}</p>
			{optionsEl}
		</div>
	);
}

function MultipleCategoricalQuestion({ id, text }: { id: number, text: string }) {

	let options: Array<Element> = [];
	let [idsChecked, setIdsChecked]: [Set<number>, (id: Set<number>) => void] = useState(new Set());

	const invertStateForId = (idToBeInverted: number) => {
		let temp = new Set(idsChecked);

		if (idsChecked.has(idToBeInverted)) {
			temp.delete(idToBeInverted);
			setIdsChecked(temp);
		} else {
			temp.add(idToBeInverted);
			setIdsChecked(temp);
		}
	};

	for (let i = 0; i < 3; i++) {
		options.push(
			(
				<div key={i}>
					<input id={'category' + (id + i).toString()} type="checkbox" onChange={() => { invertStateForId(i + id) }} checked={idsChecked.has(id + i)}></input>
					<label htmlFor={'category' + (id + i).toString()}>Test</label>
				</div >
			)
		);
	}

	return (
		<div className="card">
			<p>{text}</p>
			{options}
		</div>
	);
}

function FormulaQuestion({ text, formula, process }: FormulaQuestionType) {
	return (
		<div className="card force-shorter">
			<p>{text}: {process.execute(formula)}</p>
		</div>
	);
}

function Form() {
	let categoryId = -1;
	const processor = new Processor();

	const [worldObj, setWorldObj] = useState({});

	const addVarialble = (varName: string, value: any, aliasValue?: string) => {
		if (aliasValue != undefined) {
			value = aliasValue + "." + value;
		}

		let temp = Object.assign({}, worldObj);
		temp[varName] = value;

		setWorldObj(temp);
	};

	const addTable = (table: Object, alias?: string) => {
		if (alias != undefined) {
			alias = alias + ".";
		} else {
			alias = "";
		}
		
		let aliasedTable = {};
		
		for (const property in table) {
			aliasedTable[alias + property] = table[property];
		}
		
		console.log(aliasedTable);

		processor.addTable(aliasedTable);
	}

	const execute = (formula: string): number => {
		processor.addVariables(worldObj);
		return processor.exec(formula);
	};

	return (<>
		<Header />
		<div className="questions-field align-in-column">
			<JSONRender json={test as FormJSON} processor={{'addVariable': addVarialble, 'addTable': addTable, 'execute': execute}}/>
		</div>
	</>);
}

const root = document.getElementById('base-form');
const rootElement = createRoot(root);
rootElement.render(<Form />);