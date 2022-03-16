import BEP20_ABI from './abi/BEP20.json';
import web3 from 'web3';
import { useState } from 'react';
import { Container, Typography, Box, Button, TextField } from '@mui/material';
import { CSVLink } from 'react-csv';
import CSVReader from "react-csv-reader";
import BigNumber from 'bignumber.js';

function App() {
  const Web3_BSC = new web3('https://bsc-dataseed.binance.org/');
  const Web3_ETHER = new web3('https://speedy-nodes-nyc.moralis.io/5c2706c77e827bc97c4fe1fc/eth/mainnet')
  const [isBSC, setIsBSC] = useState(true)
  const [contract, setContract] = useState()
  const [inputAccount, setInputAccount] = useState('');
  const [listAccount, setListAccount] = useState([]);
  const [tokenAddress, setTokenAdress] = useState('')
  let listInfo = []

  const getBalance = async (address) => {
    return await contract.methods.balanceOf(address).call();
  }

  const handleForce = (data, fileInfo) => {
    data.map(async address => {
      let currBalance = await getBalance(address[0]).dividedBy(BigNumber(10).exponentiatedBy(18)).toFixed();
      listInfo.push([address[0], currBalance]);
      console.log(listInfo)
    })
  };

  const papaparseOptions = {
    header: false,
    dynamicTyping: true,
    skipEmptyLines: true,
    transformHeader: (header) => header.toLowerCase().replace(/\W/g, "_")
  };

  const hanldeSubmitToken = () => {
    try{
      if( isBSC ) {
        setContract(new Web3_BSC.eth.Contract(BEP20_ABI, tokenAddress));
      }
      else {
        setContract(new Web3_ETHER.eth.Contract(BEP20_ABI, tokenAddress));
      }
      setTokenAdress('')
      alert('Import Successful!');
    } catch(err) {
      alert('Wrong Token Address!')
    }
    
  }
  // useEffect( () => {
  //   const fetchData = async() => {
  //   const newBalance = await myContract.methods.balanceOf('0xD89BB42daE2e5fFbdE73f11967afBdD59C0a554A').call();
  //   setBalance(newBalance) };
  //   fetchData()
  // }, [])

  const toggleNetwork = () => {
    setIsBSC(!isBSC);
  }

  const handleAddAccount = async () => {
    const currBalance = await getBalance(inputAccount)/10**18;
    setListAccount([...listAccount, [inputAccount, currBalance]]);
    setInputAccount('');
  }

  const handleUpload = () => {
    setListAccount(listInfo);
  }
  // const handleFiles = async files => {
  //   var reader = new FileReader();
  //   reader.readAsText(files[0]);
  //   reader.onloadend = function(e) {
  //       // Use reader.result
  //       let addresses = reader.result.split("\"");
  //       addresses = addresses.filter(address => address !== '\n' && address !== ' ' && address !== '');
  //       console.log(addresses.length)
  //       addresses.map(async (address) => {
  //         let currBalance = await getBalance(address)/10**18;
  //         listInfo.push([address, currBalance]);
  //       })
  //   }
  // }

  return (
    <Container>
      <Typography align='center' variant="h2" style={{ paddingTop: '20px'}}>Get Balance App</Typography>
      {isBSC ?
        <Button variant="contained" style={{height: '50px', backgroundColor: 'orange', width: '40%', margin: '0 auto', display: 'block'}} onClick={toggleNetwork} >BSC</Button>
        : <Button variant="contained" style={{height: '50px', backgroundColor: 'black', width: '40%', margin: '0 auto' , display: 'block'}} onClick={toggleNetwork} >Ethereum</Button>
      }
      <Box style={{display: 'flex', justifyContent: 'space-between', width: '100%', margin: '20px auto', paddingBottom: '10px'}}>
        <TextField id="filled-basic" label="Token Address" variant="filled" value={tokenAddress} onChange={e => setTokenAdress(e.target.value)} />
        <Button variant="contained" style={{height: '50px'}} onClick={hanldeSubmitToken}>Submit</Button>
        <TextField id="standard-basic" label="Account Address" variant="standard" value={inputAccount} onChange={(e) => setInputAccount(e.target.value)}/>
        <Button variant="contained" style={{height: '50px'}} onClick={handleAddAccount}>Add Account</Button>
        <CSVReader
          cssClass="react-csv-input"
          onFileLoaded={handleForce}
          parserOptions={papaparseOptions}
        />
        <Button variant="contained" style={{height: '20px'}} onClick={handleUpload}>Upload</Button>
      </Box>
      <Box style={{height: '50px', backgroundColor: 'green', width: '40%', margin: '0 auto', borderRadius:'5px', display:'flex', justifyContent:'center', alignItems: 'center'}}>
        <CSVLink data={listAccount}>Download me</CSVLink>
      </Box>
      {listAccount.map((acc, id) => { 
        return (<Typography key={id} align='center' variant="h2" style={{fontSize: '16px', marginBottom: '7px'}}>{acc[0].slice(0,15)}...... has {acc[1]}</Typography>)
      })}
    </Container>
  );
}

export default App;
