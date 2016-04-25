<?php
$filename = "bilet_na_koncert.pdf";
if (!isset($tickets)) {
global $tickets;
 $tickets = array(
	array(
		'nr_rezerwacji' => "666_69",
		'kod_rezerwacji' => "4636457573457347474745373474",
		'cena' => 1000,
		'tytul' => "Koncert zespołu zdaj magisterkę!",
		'data' => time(),
		'adres' => "Politechnika Poznańska, Sala 230\nPoznań, Piotrowo 69",
		'wlasciciel' => "Jan Nowak-Jeziorański",
		'miejsce' => "Piętro: 0\nMiejsce: -1\nRząd: G"
	),
	array(
		'nr_rezerwacji' => "666_70",
		'kod_rezerwacji' => "23487234587238572893578923",
		'cena' => 1000,
		'tytul' => "Koncert zespołu zdaj magisterkę!",
		'data' => time(),
		'adres' => "Politechnika Poznańska, Sala 230\nPoznań, Piotrowo 69",
		'wlasciciel' => "Ewelina Piękna-Rajska",
		'miejsce' => "Piętro: 0\nMiejsce: -1\nRząd: G"
	),
	array(
		'nr_rezerwacji' => "666_71",
		'kod_rezerwacji' => "45289248944526484233228",
		'cena' => 1000,
		'tytul' => "Koncert zespołu zdaj magisterkę!",
		'data' => time(),
		'adres' => "Politechnika Poznańska, Sala 230\nPoznań, Piotrowo 69",
		'wlasciciel' => "Jakub Puchatek",
		'miejsce' => "Piętro: 0\nMiejsce: -1\nRząd: G"
	)
);
}
//-------------------------------------------
require('PDF/fpdf.php');
require('PDF/fpdi.php');
require('PDF/qrcode.class.php');

class PDF extends FPDF
{
	function Footer() 	{
		// Position at 1.5 cm from bottom
		$this->SetY(-15);
		// Arial italic 8
		$this->SetFont('Arial','I',8);
		// Page number
		$this->Cell(0,10,'Dokument wygenerowany elektronicznie.',0,0,'L');
		$this->Cell(0,10,'Strona '.$this->PageNo().'/{nb}',0,0,'C');
		$this->Cell(0,10,$filename,0,0,'R');
	}
}

// initiate FPDI 
$pdf =& new FPDI(); 
$pdf->SetLeftMargin(24);
$pdf->SetRightMargin(24);

$pdf->AddFont('Arial','','arial.php');
$pdf->AddFont('Arial','B','arialbd.php');
$pdf->SetTitle("Bilet internetowy");
$pdf->SetAuthor('TwojBilet.pl');
$pdf->SetCreator('TicketPrinter by Koko Software');

// set the sourcefile 
$pdf->setSourceFile('/vagrant_nox/TwojBilet.pdf'); 
// import page 1 
$tplIdx = $pdf->importPage(1); 


	foreach ($tickets as $ticket) {
		// add a page 
		$pdf->AddPage(); 
		$pdf->useTemplate($tplIdx, 0, 0); 

		// now write some text above the imported page 
		$pdf->SetFont('Arial'); 
		//$pdf->SetTextColor(255,0,0); 
		$pdf->SetY(33); 
		$pdf->Write(5, "Numer rezerwacji: ".$ticket['nr_rezerwacji']); 
		// Line break
		$pdf->Ln();
		$pdf->Write(10, $ticket['kod_rezerwacji']); 
		$pdf->SetY(62); 
		$pdf->Cell(0,5, iconv('UTF-8','iso-8859-2//TRANSLIT//IGNORE',"Cena: ".number_format($ticket['cena'],2)." zł"), 0, 1, 'R'); 

		$pdf->SetFont('', 'B', 20); 
		$pdf->Write(20, iconv('UTF-8','iso-8859-2//TRANSLIT//IGNORE',$ticket['tytul'])); 

		$pdf->SetFont('', '', 12); 
		$pdf->SetXY(24,82);
		$tekst = $ticket['data']."\n\n".$ticket['adres']."\n\nWłaściciel rezerwacji: ".$ticket['wlasciciel']."\n\n".$ticket['miejsce'];
		$pdf->MultiCell(100, 5,iconv('UTF-8','iso-8859-2//TRANSLIT//IGNORE',$tekst), 0, 'L');

		$data = "<code>".$ticket['kod_rezerwacji']."</code><id>".$ticket['nr_rezerwacji']."</id><event>".$ticket['tytul']."</event><client>".$ticket['wlasciciel']."</client><time>".$ticket['data']."</time>";
		$code = "<ticket>$data<hash>".hash('sha256',$data.'Szukasz moze jakiejs soli? Lezy na stole.')."</hash></ticket>";
		$qrcode = new QRcode($code, 'L'); // error level : L, M, Q, H
		$qrcode->displayFPDF($pdf, 125, 84, 60);
	}
	
header("Content-Type: application/pdf");
$pdf->Output($filename, 'D'); 
?>
