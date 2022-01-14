import { makeStyles } from '@mui/styles';

export default makeStyles((theme) => ({
  paper: {
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    position: 'absolute',
    width: 500,
    backgroundColor: "white",
    padding: '40px',
    borderRadius: '20px',
    minHeight: '50%',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
  },
  header: {
    margin: '0 0 10px 0',
  },
  title: {
    marginBottom: '10px',
    marginTop: '15px'
  },
  textarea: {
    padding: '10px',
    marginBottom: '10px',
  },
  footer: {
    display: 'flex',
    justifyContent: 'space-between',
    marginTop: '10px',
  },
}));