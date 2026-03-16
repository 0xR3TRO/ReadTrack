import api from "./api";

export const getNotes = async (bookId) => {
    const response = await api.get(`/books/${bookId}/notes`);
    return response.data;
};

export const createNote = async (bookId, data) => {
    const response = await api.post(`/books/${bookId}/notes`, data);
    return response.data;
};

export const updateNote = async (bookId, noteId, data) => {
    const response = await api.put(`/books/${bookId}/notes/${noteId}`, data);
    return response.data;
};

export const deleteNote = async (bookId, noteId) => {
    const response = await api.delete(`/books/${bookId}/notes/${noteId}`);
    return response.data;
};
