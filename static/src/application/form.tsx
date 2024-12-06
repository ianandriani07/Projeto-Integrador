import "../styles/form.scss";
import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { Header } from "../components/Header.tsx";
import { Processor, DefaultFunctions } from "../js/processor.ts";

interface ProcessorFunctions {
	addVariable: (varName: string, value: any, aliasValue?: string) => void,
	addTable: (table: Object, alias?: string) => void,
	execute: (formula: string) => number,
	init: (varName: string, value: any, aliasValue?: string) => void,
}

enum QuestionType {
	SingleCategoricalQuestion = 'objetva',
	Formula = "formula",
	Numeric = 'numerica',
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
	formulaName: string,
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
	nome_variavel: string,
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
	json?: FormJSON,
	processor: ProcessorFunctions
}

function saveAnswerAndRedirect(worldObj: object) {
	const correctFormat = ([key, value]: [string, string]) => {
		return {
			"nome_variavel": key,
			"resposta": value.slice(key.length + 1)
		};
	};

	fetch('/responder-perguntas', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(Object.entries(worldObj).map(correctFormat))
	}).then(() => {
		location.reload();
	}
	);
}

function JSONRender({ json, processor }: RenderJSON) {
	let rendered: Array<Element> = [];
	let id = 0;

	if (json == undefined) {
		return (
			<></>
		);
	}

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
							<FormulaQuestion text={q.texto} formula={q.formula} process={processor} formulaName={q.nome_variavel} />
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
	let [idChecked, setIdChecked] = useState(-1);

	processor.addTable(conversionTable, varName);
	processor.init(varName, 'undefined', varName);

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

function FormulaQuestion({ text, formula, formulaName, process }: FormulaQuestionType) {
	let output = process.execute(formula);
	process.addVariable(formulaName, output);

	return (
		<div className="card force-shorter">
			<p>{text}: {output}</p>
		</div>
	);
}

function Form() {
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

		processor.addTable(aliasedTable);
	}

	const execute = (formula: string): number => {
		processor.addVariables(worldObj);
		return processor.exec(formula);
	};

	const init = (varName: string, value: any, aliasValue?: string) => {
		if (aliasValue != undefined) {
			value = aliasValue + "." + value;
		}

		processor.addVariable(varName, value);
	};

	const processor_functions = { 'addVariable': addVarialble, 'addTable': addTable, 'execute': execute, 'init': init };

	const [form, setForm] = useState(undefined);

	useEffect(() => {
		fetchQuestion();
	}, []);

	const fetchQuestion = async () => {
		try {
			const response = await fetch(`/perguntas/formulario/${window.id_form}?pagina=1&por_pagina=10`);
			const result = await response.json();
			setForm(result as FormJSON);
		} catch (error) {
			console.error("Bruh, you fucked up. The form_id don't exist in the backend. Or maybe you're trash...");
		}
	};

	return (<>
		<Header logout={false} return_link={window.url_to_return} />
		<div className="questions-field align-in-column">
			<JSONRender json={form} processor={processor_functions} />
			<a className="save-button rounded-borders-20px" onClick={() => { saveAnswerAndRedirect(worldObj) }}>Salvar</a>
		</div>
	</>);
}

const root = document.getElementById('base-form');
const rootElement = createRoot(root);
rootElement.render(<Form />);