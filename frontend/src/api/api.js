import axios from "axios";
//"API WITH FLASK"

const api = axios.create({
    baseURL: "http://jarvis.altarede.com.br",
})

export default api