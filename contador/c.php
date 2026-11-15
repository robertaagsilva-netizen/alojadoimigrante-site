<?php
// Contador simples da Loja do Imigrante.
// Guarda só números por dia e por evento. Não guarda IP, nome nem nenhum dado pessoal.
header('Cache-Control: no-store');
header('Content-Type: text/plain; charset=utf-8');

$e = isset($_POST['e']) ? $_POST['e'] : (isset($_GET['e']) ? $_GET['e'] : '');
if (!preg_match('/^[a-z0-9_]{2,40}$/', $e)) { http_response_code(204); exit; }

$dir = __DIR__ . '/dados';
if (!is_dir($dir)) { @mkdir($dir, 0755, true); }
$file = $dir . '/contagens.json';
$dia = gmdate('Y-m-d', time() + 3600); // hora de Espanha/Portugal continental (aprox.)

$fp = @fopen($file, 'c+');
if (!$fp) { http_response_code(204); exit; }
if (flock($fp, LOCK_EX)) {
  $raw = stream_get_contents($fp);
  $data = $raw ? json_decode($raw, true) : array();
  if (!is_array($data)) { $data = array(); }
  if (!isset($data[$dia])) { $data[$dia] = array(); }
  // limite de segurança: no máximo 120 eventos diferentes por dia
  if (isset($data[$dia][$e]) || count($data[$dia]) < 120) {
    $data[$dia][$e] = (isset($data[$dia][$e]) ? $data[$dia][$e] : 0) + 1;
  }
  // guarda só os últimos 400 dias
  if (count($data) > 400) { ksort($data); $data = array_slice($data, -400, null, true); }
  ftruncate($fp, 0); rewind($fp);
  fwrite($fp, json_encode($data));
  fflush($fp);
  flock($fp, LOCK_UN);
}
fclose($fp);
http_response_code(204);
