import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Books from "./pages/Books";
import BookDetail from "./pages/BookDetail";
import AddBook from "./pages/AddBook";
import Authors from "./pages/Authors";
import AuthorDetail from "./pages/AuthorDetail";
import AddAuthor from "./pages/AddAuthor";
import "./styles/App.css";

function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <div className="app">
                    <Navbar />
                    <main className="main-content">
                        <Routes>
                            <Route path="/login" element={<Login />} />
                            <Route path="/register" element={<Register />} />
                            <Route
                                path="/"
                                element={
                                    <ProtectedRoute>
                                        <Home />
                                    </ProtectedRoute>
                                }
                            />
                            <Route
                                path="/books"
                                element={
                                    <ProtectedRoute>
                                        <Books />
                                    </ProtectedRoute>
                                }
                            />
                            <Route
                                path="/books/new"
                                element={
                                    <ProtectedRoute>
                                        <AddBook />
                                    </ProtectedRoute>
                                }
                            />
                            <Route
                                path="/books/:id"
                                element={
                                    <ProtectedRoute>
                                        <BookDetail />
                                    </ProtectedRoute>
                                }
                            />
                            <Route
                                path="/books/:id/edit"
                                element={
                                    <ProtectedRoute>
                                        <AddBook />
                                    </ProtectedRoute>
                                }
                            />
                            <Route
                                path="/authors"
                                element={
                                    <ProtectedRoute>
                                        <Authors />
                                    </ProtectedRoute>
                                }
                            />
                            <Route
                                path="/authors/new"
                                element={
                                    <ProtectedRoute>
                                        <AddAuthor />
                                    </ProtectedRoute>
                                }
                            />
                            <Route
                                path="/authors/:id"
                                element={
                                    <ProtectedRoute>
                                        <AuthorDetail />
                                    </ProtectedRoute>
                                }
                            />
                            <Route
                                path="/authors/:id/edit"
                                element={
                                    <ProtectedRoute>
                                        <AddAuthor />
                                    </ProtectedRoute>
                                }
                            />
                        </Routes>
                    </main>
                </div>
            </AuthProvider>
        </BrowserRouter>
    );
}

export default App;
