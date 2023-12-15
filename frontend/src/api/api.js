import axios from "axios";
//"API WITH FLASK"

const api = axios.create({
    baseURL: "http://187.16.255.78:5000",
})

export default api
