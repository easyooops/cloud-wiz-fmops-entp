const restApi = () => {

    const API_ENDPOINT = import.meta.env.VITE_API_ENDPOINT

    const call = async (url: string, method: string, header: any, body: any): object => {
        const response: any = await useFetch(`${API_ENDPOINT}${url}`, {
            method: method,
            headers: header == null ? {'Content-Type': 'application/json'} : header,
            param: JSON.stringify(body),
        });
        return response
    }

    const get = (url: string, param: any, header: any) => {
        return call(url, 'get', null, param)
    };

    const post = (url: string, body: object, header: any) => {
        return call(url, 'post', header, body)
    };

    return { get, post }
};
export default restApi;
