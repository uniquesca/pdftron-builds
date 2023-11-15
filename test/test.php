<?php

require_once 'LicenseKey.php';

global $LicenseKey;
PDFNet::Initialize($LicenseKey);
PDFNet::GetSystemFontList();

$testFilesDir = getcwd() . '/test_files/';

//--------------------------------------------------------------------------------
// Update a business card template with personalized info
$doc = new PDFDoc($testFilesDir . 'card_template.pdf');
$doc->InitSecurityHandler();

// first, replace the image on the first page
$replacer = new ContentReplacer();
$page     = $doc->GetPage(1);
$img      = Image::Create($doc->GetSDFDoc(), $testFilesDir . 'peppers.jpg');
$replacer->AddImage($page->GetMediaBox(), $img->GetSDFObj());
// next, replace the text placeholders on the second page
$replacer->AddString('NAME', 'John Smith');
$replacer->AddString('QUALIFICATIONS', 'Philosophy Doctor');
$replacer->AddString('JOB_TITLE', 'Software Developer');
$replacer->AddString('ADDRESS_LINE1', '#100 123 Software Rd');
$replacer->AddString('ADDRESS_LINE2', 'Vancouver, BC');
$replacer->AddString('PHONE_OFFICE', '604-730-8989');
$replacer->AddString('PHONE_MOBILE', '604-765-4321');
$replacer->AddString('EMAIL', 'info@pdftron.com');
$replacer->AddString('WEBSITE_URL', 'http://www.pdftron.com');
// finally, apply
$replacer->Process($page);

$doc->Save($testFilesDir . 'result.pdf', 0);
echo nl2br("Done. Result saved in result.pdf\n");
