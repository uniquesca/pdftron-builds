<?php
// License key is provided via the PDFTRON_LICENSE_KEY environment variable
// (in CI it comes from the repository secret of the same name).
// Obtain a key at https://www.pdftron.com/pws/get-key (demo) or https://www.pdftron.com/form/contact-sales (production).
$LicenseKey = getenv('PDFTRON_LICENSE_KEY');
if ($LicenseKey === false || $LicenseKey === '') {
    throw new Exception('Please set the PDFTRON_LICENSE_KEY environment variable to your PDFTron license key.');
}
