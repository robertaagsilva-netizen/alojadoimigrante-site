<?php
// Recebe os contatos que o ManyChat manda (ação "Solicitação externa").
// Endereço: /painel/lead.php?t=TOKEN
// Guarda nome, @ do Instagram, palavra-chave e hora. Nada mais.
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');
$TOKEN_HASH = '27ceca4fd15fbee50f45b143c8ecd80f2992378c60b53a909a793d1b6e8678ad';
$t = isset($_GET['t']) ? $_GET['t'] : '';
if (!hash_equals($TOKEN_HASH, hash('sha256', $t))) { http_response_code(404); exit; }

$raw = file_get_contents('php://input');
$in = json_decode($raw, true);
if (!is_array($in)) $in = $_POST;
function campo($in, $k, $max = 80) {
  $v = isset($in[$k]) ? trim((string)$in[$k]) : '';
  $v = preg_replace('/[\x00-\x1F\x7F]/u', '', $v);
  return mb_substr($v, 0, $max);
}
$lead = array(
  'quando' => time(),
  'nome' => campo($in, 'nome'),
  'usuario' => ltrim(campo($in, 'usuario', 40), '@'),
  'palavra' => mb_strtoupper(campo($in, 'palavra', 30)),
  'canal' => campo($in, 'canal', 20) ?: 'Instagram',
);
if ($lead['nome'] === '' && $lead['usuario'] === '') { http_response_code(204); exit; }

$dir = __DIR__ . '/dados';
if (!is_dir($dir)) @mkdir($dir, 0755, true);
$fp = @fopen($dir . '/contatos.jsonl', 'a');
if ($fp) { flock($fp, LOCK_EX); fwrite($fp, json_encode($lead, JSON_UNESCAPED_UNICODE) . "\n"); flock($fp, LOCK_UN); fclose($fp); }
header('Content-Type: application/json');
echo '{"ok":true}';
