import api from "./api";

export async function getAICoach() {

    const response = await api.get("/ai/recommend");

    return response.data;

}