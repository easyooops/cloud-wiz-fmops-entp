const restApi = () => {

    const API_ENDPOINT = import.meta.env.VITE_API_ENDPOINT + '/api/v1';

    const get = async (url: string, param: any, header: any): Promise<object> => {
        return await useFetch(`${API_ENDPOINT}${url}`, {
            method: 'GET',
            headers: header == null ? {'Content-Type': 'application/json'} : header
        });
    };

    const post = async (url: string, body: any, header: any): Promise<object> => {
        return await useFetch(`${API_ENDPOINT}${url}`, {
            method: 'POST',
            headers: header == null ? {'Content-Type': 'application/json'} : header,
            body: JSON.stringify(body)
        });
    };

    return { get, post }
};
export default restApi;
