import axios from 'axios';

const URL = 'http://localhost:5000'

export const getAccount = (payload) => axios.get(`${URL}/account`, payload);