import api from "./api";

export const getFiles = async (bookId) => {
    const response = await api.get(`/books/${bookId}/files`);
    return response.data;
};

export const uploadFile = async (bookId, file) => {
    const formData = new FormData();
    formData.append("file", file);
    const response = await api.post(`/books/${bookId}/files`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
};

export const downloadFile = async (bookId, fileId) => {
    const response = await api.get(`/books/${bookId}/files/${fileId}`, {
        responseType: "blob",
    });
    return response;
};

export const deleteFile = async (bookId, fileId) => {
    const response = await api.delete(`/books/${bookId}/files/${fileId}`);
    return response.data;
};
