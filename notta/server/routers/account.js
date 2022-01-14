import express from 'express';
import { getAccount, createAccount } from '../controllers/account.js'

const router = express.Router();

router.post('/logIn', getAccount);

router.post('/createAcount', createAccount)

export default router;