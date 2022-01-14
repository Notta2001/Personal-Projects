import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import mongoose from 'mongoose';
import account from './routers/account.js'
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

const URL = 'mongodb+srv://admin:lemongreentea@cluster0.wo7la.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

app.use(bodyParser.json({ limit: '30mb' }));
app.use(bodyParser.urlencoded({ extended: true, limit: '30mb' }));
app.use(cors());

app.use('/account', account);

mongoose.connect(URL, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => {
        console.log('Connected to DB');
    }).catch(err => {
        console.log('err', err)
    })


app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});