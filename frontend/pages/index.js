import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

const measureTypes = ["manga","cuello"]

export default function Home() {
  return (
      <Box
        component="form"
        sx={{
          '& > :not(style)': { m: 1, width: '25ch' },
        }}
        noValidate
        autoComplete="off"
      >
        {
          measureTypes.map((element)=>{
            <TextField key={"measureType-"+element}id="ref-text" label="Referencia" variant="outlined" />
          })
        }
      </Box>
  )
}
