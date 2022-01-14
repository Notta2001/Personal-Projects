import { AccountModel } from '../models/AccountModel.js'

export const getAccount = async (req, res) => {
    try {
        // const newAccount = new AccountModel({
        //     userName: 'admin',
        //     password: '123456789',
        //     name: 'notta',
        // })

        // newAccount.save();

        const currAccount = req.body;
        const account = await AccountModel.find({ userName: currAccount.userName });
        console.log(req.body)

        res.status(200).json(account);
    } catch(err) {
        res.status(500).json({ error: err })
    }
};

export const createAccount = async (req, res) => {
    try { 
        const newAccount = req.body;

        const account = new AccountModel(newAccount);
        await account.save();

        res.status(200).json(account);
    } catch (err) {
        res.status(500).json({ error: err})
    }
};