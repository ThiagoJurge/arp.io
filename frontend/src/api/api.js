import axios from "axios";
//"API WITH FLASK"

const api = axios.create({
    baseURL: "http://localhost:81",
})

export default api