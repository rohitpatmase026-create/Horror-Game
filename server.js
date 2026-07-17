const express = require("express");
const multer = require("multer");
const cors = require("cors");

const app = express();

app.use(cors());

const upload = multer({
    dest: "uploads/"
});

app.post("/convert/word", upload.single("file"), (req,res)=>{

    console.log(req.file);

    res.sendFile(__dirname + "/sample.docx");

});

app.post("/convert/excel", upload.single("file"), (req,res)=>{

    console.log(req.file);

    res.sendFile(__dirname + "/sample.xlsx");

});

app.listen(3000,()=>{
    console.log("Server Running");
});
