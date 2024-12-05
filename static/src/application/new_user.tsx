import "../styles/new_user.scss";
const React = require('react');
const { createRoot } = require('react-dom/client');
import { Header } from "../components/Header.tsx";

function Hub({ children, activeTab, setActiveTab }) {
    return (
        <main className="center hub gray-background rounded-borders-20px">
        <nav className="tabs">
            <button className={activeTab === "add" ? "tab active" : "tab"} onClick={() => setActiveTab("add")}>
                Adicionar
            </button>
            <button className={activeTab === "edit" ? "tab active" : "tab"} onClick={() => setActiveTab("edit")}>
                Editar
            </button>
            <button className={activeTab === "delete" ? "tab active" : "tab"} onClick={() => setActiveTab("delete")}>
                Excluir
            </button>
        </nav>
        <section className="tab-content">
            {children}
        </section>
    </main>
    );
}

function UserForm({ onSubmit }) {
    return (
        <form className="user-form" onSubmit={onSubmit}>
            <div className="form-group">
                <label htmlFor="name">Nome:</label>
                <input type="text" id="name" name="name" placeholder="Digite o nome" required />
            </div>
            <div className="form-group">
                <label htmlFor="email">Email:</label>
                <input type="email" id="email" name="email" placeholder="Digite o email" required />
            </div>
            <div className="form-group">
                <label htmlFor="password">Senha:</label>
                <input type="password" id="password" name="password" placeholder="Digite a senha" required />
            </div>
            <div className="form-group">
                <button type="submit" className="btn">Criar Usuário</button>
            </div>
        </form>
    );
}

function EditForm({ onSubmit }) {
    return (
        <form className="edit-form" onSubmit={onSubmit}>
            <div className="form-group">
                <label htmlFor="userId">ID do Usuário:</label>
                <input type="text" id="userId" name="userId" placeholder="Digite o ID do usuário" required />
            </div>
            <div className="form-group">
                <label htmlFor="newName">Novo Nome:</label>
                <input type="text" id="newName" name="newName" placeholder="Digite o novo nome" />
            </div>
            <div className="form-group">
                <label htmlFor="newEmail">Novo Email:</label>
                <input type="email" id="newEmail" name="newEmail" placeholder="Digite o novo email" />
            </div>
            <div className="form-group">
                <button type="submit" className="btn">Atualizar Usuário</button>
            </div>
        </form>
    );
}

function DeleteForm({ onSubmit }) {
    return (
        <form className="delete-form" onSubmit={onSubmit}>
            <div className="form-group">
                <label htmlFor="userId">ID do Usuário:</label>
                <input type="text" id="userId" name="userId" placeholder="Digite o ID do usuário" required />
            </div>
            <div className="form-group">
                <button type="submit" className="btn">Excluir Usuário</button>
            </div>
        </form>
    );
}

function NewUser() {
    const [activeTab, setActiveTab] = React.useState("add");

    const handleSubmit = (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());
        console.log("Form Data:", data);
    };

    const renderContent = () => {
        switch (activeTab) {
            case "add":
                return <UserForm onSubmit={handleSubmit} />;
            case "edit":
                return <EditForm onSubmit={handleSubmit} />;
            case "delete":
                return <DeleteForm onSubmit={handleSubmit} />;
            default:
                return null;
        }
    };

    return (
        <>
            <Header title="Gerenciar Usuários" />
            <Hub activeTab={activeTab} setActiveTab={setActiveTab}>
                {renderContent()}
            </Hub>
        </>
    );
}

const root = document.getElementById('base-new-user');
const rootElement = createRoot(root);
rootElement.render(<NewUser />);
