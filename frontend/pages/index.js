import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import VideoStreaming from '../components/videoStreaming';
import { DataGrid} from '@mui/x-data-grid';

const columns = [
  {field:'measure_type',headerName:'TIPO DE MEDIDA',width:150,editable:false},
  {field:'sewing_measure', headerName:'Medida costura',width:150, editable:true},
  {field:'fineshed_measure', headerName:'Medida terminado',width:160,editable:true}
]
const measureTypes = [
    {id:1,measure_type:'Banda',sewing_measure:'',finished_measure:''},
    {id:2,measure_type:'Ancho pecho',sewing_measure:'',finished_measure:''},
    {id:3,measure_type:'Contorno pecho',sewing_measure:'',finished_measure:''},
    {id:4,measure_type:'Contorno Ruedo',sewing_measure:'',finished_measure:''},
    {id:5,measure_type:'Largo centro frente',sewing_measure:'',finished_measure:''},
    {id:6,measure_type:'Largo total x el frente',sewing_measure:'',finished_measure:''},
    {id:7,measure_type:'Altura bolsillo',sewing_measure:'',finished_measure:''},
    {id:8,measure_type:'Largo frente hombro',sewing_measure:'',finished_measure:''},
    {id:9,measure_type:'Hombro 1',sewing_measure:'',finished_measure:''},
    {id:10,measure_type:'Hombro 2',sewing_measure:'',finished_measure:''},
    {id:11,measure_type:'Sisa 1',sewing_measure:'',finished_measure:''},
    {id:12,measure_type:'Sisa 2',sewing_measure:'',finished_measure:''},
    {id:13,measure_type:'Largo de manga 1',sewing_measure:'',finished_measure:''},
    {id:14,measure_type:'Largo de manga 2',sewing_measure:'',finished_measure:''},
    {id:15,measure_type:'Biceps',sewing_measure:'',finished_measure:''},
    {id:16,measure_type:'Hombro a hombro',sewing_measure:'',finished_measure:''},
    {id:17,measure_type:'Ancho espalda',sewing_measure:'',finished_measure:''},
    {id:18,measure_type:'Largo centro espalda',sewing_measure:'',finished_measure:''},
    {id:19,measure_type:'Largo de mana C.E',sewing_measure:'',finished_measure:''}
  ]

export default function Home() {
  return (
    <>
      <Box
        component="form"
        sx={{
          '& > :not(style)': { m: 1, width: '25ch' },
        }}
        noValidate
        autoComplete="off"
      >
        {/* {
          measureTypes.map((element)=>{
            <TextField key={"measureType-"+element}id="ref-text" label="Referencia" variant="outlined" />
          })
        } */}
       
        {/* <VideoStreaming></VideoStreaming> */}
      </Box>
       <Box sx={{ height: 400, width:'600px'}}>
       <DataGrid
         rows={measureTypes}
         columns={columns}
         pageSize={10}
         rowsPerPageOptions={[10]}
         disableSelectionOnClick
         experimentalFeatures={{ newEditingApi: true }}
       />
     </Box>
     </>
  )
}
