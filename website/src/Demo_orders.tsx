import React from "react";
import { patientData, PatientName } from "./patientData";
import {
  Typography,
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  TableContainer,
  Table,
  TableBody,
  TableRow,
  TableCell,
  DialogActions,
  Paper,
  Button,
} from "@mui/material";
import { DataGrid, GridColDef, GridRowParams } from "@mui/x-data-grid";

interface Orders {
  name: string;
  category: string;
  dose: string;
  route: string;
  frequency: string;
  indication: string;
  status: string;
  date_ordered: string;
  date_start: string;
  date_end: string;
  is_ongoing_for_discharge: boolean;
}

interface PatientOrdersProps {
  patient: PatientName;
}

export default function Orders(props: PatientOrdersProps) {
  const { medication_orders } = patientData[props.patient];

  // State to control the dialog
  const [open, setOpen] = React.useState(false);
  const [selectedOrder, setSelectedOrder] = React.useState<Orders | null>(null);

  // Define columns for DataGrid
  const columns: GridColDef[] = [
    { field: "name", headerName: "Medication Name", flex: 1 },
    { field: "status", headerName: "Status", flex: 1 },
    { field: "date_ordered", headerName: "Date Ordered", flex: 1 },
    { field: "date_start", headerName: "Date Start", flex: 1 },
    { field: "date_end", headerName: "Date End", flex: 1 },
  ];

  // Open dialog with selected order details
  const handleRowClick = (params: GridRowParams) => {
    setSelectedOrder(params.row as Orders);
    setOpen(true);
  };

  const handleCloseDialog = () => {
    setOpen(false);
    setSelectedOrder(null);
  };

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" color="Black" gutterBottom>
        Orders
      </Typography>

      {/* DataGrid for displaying orders */}
      <Box sx={{ height: 600, width: "100%" }}>
        <DataGrid
          rows={medication_orders}
          columns={columns}
          pageSizeOptions={[5, 10]}
          onRowClick={handleRowClick}
          disableRowSelectionOnClick
          getRowId={(row) => row.name}
          sx={{
            backgroundColor: "rgba(255, 255, 255, 0.5)",
            "& .MuiDataGrid-cell": {
              fontSize: "1rem", // font size
              borderBottom: "2px solid rgba(0, 0, 0, 0.12)", // thicker row divider
            },
            "& .MuiDataGrid-columnHeaderTitle": {
              fontSize: "1.1rem", // header size
              fontWeight: "bold", // header bold
            },
            "& .MuiDataGrid-columnSeparator": {
              display: "block",
              borderRightWidth: "2px !important", // thicker column divider
            },
          }}
        />
      </Box>

      <Dialog open={open} onClose={handleCloseDialog} fullWidth maxWidth="sm">
        <DialogTitle color="white" sx={{ fontWeight: "bold" }}>
          {selectedOrder?.name} ({selectedOrder?.dose})
        </DialogTitle>
        <DialogContent>
          <TableContainer component={Paper} sx={{ backgroundColor: "white" }}>
            <Table>
              <TableBody>
                <TableRow>
                  <TableCell>
                    <b>Medication Name:</b>
                  </TableCell>
                  <TableCell>{selectedOrder?.name}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>
                    <b>Medication Category:</b>
                  </TableCell>
                  <TableCell>{selectedOrder?.category}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>
                    <b>Dose:</b>
                  </TableCell>
                  <TableCell>{selectedOrder?.dose}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>
                    <b>Route:</b>
                  </TableCell>
                  <TableCell>{selectedOrder?.route}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>
                    <b>Frequency:</b>
                  </TableCell>
                  <TableCell>{selectedOrder?.frequency}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>
                    <b>Indication:</b>
                  </TableCell>
                  <TableCell>{selectedOrder?.indication}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>
                    <b>Status:</b>
                  </TableCell>
                  <TableCell>{selectedOrder?.status}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>
                    <b>Date Ordered:</b>
                  </TableCell>
                  <TableCell>{selectedOrder?.date_ordered}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>
                    <b>Date Start:</b>
                  </TableCell>
                  <TableCell>{selectedOrder?.date_start}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>
                    <b>Date End:</b>
                  </TableCell>
                  <TableCell>{selectedOrder?.date_end}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>
                    <b>Ongoing for Discharge:</b>
                  </TableCell>
                  <TableCell>
                    {selectedOrder?.is_ongoing_for_discharge ? "Yes" : "No"}
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} color="primary">
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
