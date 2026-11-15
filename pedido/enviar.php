<?php
// Recebe o formulário de pedido, guarda as respostas (pasta protegida) e abre o pagamento no Stripe.
header('Cache-Control: no-store');
$PAG = array(
  'rp'    => 'https://buy.stripe.com/bJe14pgEq4ab5Zpd0d0VO04',  // residência permanente 125 €
  'nie'   => 'https://buy.stripe.com/dRmcN787UeOPevV1hv0VO05',  // NIE 115 €
  'indef' => 'https://buy.stripe.com/28E28tcoa7mn3Rh0dr0VO06',  // indeferido 195 €
  'casam' => 'https://wa.me/351935149920?text=' . rawurlencode('Olá! Acabei de fazer o meu pedido no site: quero registrar o meu casamento no Brasil.'),
  'reag'  => 'https://buy.stripe.com/28E6oJ73QeOPcnNbW90VO0b',  // consultoria 35 €
  'outro' => 'https://buy.stripe.com/28E6oJ73QeOPcnNbW90VO0b',  // consultoria 35 €
);
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: ./', true, 303); exit; }
function campo($k, $max) { $v = isset($_POST[$k]) ? trim((string)$_POST[$k]) : ''; $v = preg_replace('/[\x00-\x1F\x7F]+/u', ' ', $v); return mb_substr($v, 0, $max, 'UTF-8'); }
$s = campo('servico', 10);
if (!isset($PAG[$s])) { header('Location: ./', true, 303); exit; }
if (campo('site', 50) !== '') { header('Location: ' . $PAG[$s], true, 303); exit; } // robô
$p = array(
  'quando' => gmdate('Y-m-d H:i', time() + 3600),
  'servico' => $s,
  'nome' => campo('nome', 80),
  'whatsapp' => campo('whatsapp', 25),
  'email' => campo('email', 100),
  'primeiro_titulo' => campo('primeiro_titulo', 7),
  'sem_buraco' => campo('sem_buraco', 8),
  'em_dia' => campo('em_dia', 8),
  'portugues' => campo('portugues', 8),
  'cidade' => campo('cidade', 60),
  'caso' => campo('caso', 800),
);
if (strlen($p['nome']) >= 2 && strlen(preg_replace('/\D/', '', $p['whatsapp'])) >= 8 && campo('aceito', 2) === '1') {
  $dir = dirname(__DIR__) . '/contador/dados';
  if (!is_dir($dir)) @mkdir($dir, 0755, true);
  @file_put_contents($dir . '/pedidos.jsonl', json_encode($p, JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);
}
header('Location: ' . $PAG[$s], true, 303);
