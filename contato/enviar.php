<?php
// Recebe o formulário de contato, guarda uma cópia (pasta protegida) e manda um e-mail para a Loja.
header('Cache-Control: no-store');
$PARA = 'alojadoimigrante.pt@gmail.com';
$DE_SITE = 'contato@alojadoimigrante.com';
$TIPOS = array('servico' => 'SERVIÇO', 'parceria' => 'PARCERIA', 'divulgacao' => 'DIVULGAÇÃO', 'imprensa' => 'IMPRENSA', 'outro' => 'OUTRO');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /contato/', true, 303); exit; }
function campo($k, $max, $linhas = false) {
  $v = isset($_POST[$k]) ? trim((string)$_POST[$k]) : '';
  $v = $linhas ? preg_replace('/[\x00-\x09\x0B\x0C\x0E-\x1F\x7F]+/u', ' ', $v) : preg_replace('/[\x00-\x1F\x7F]+/u', ' ', $v);
  return mb_substr($v, 0, $max, 'UTF-8');
}
$ok = '/contato/?ok=1';
// robôs: campo escondido preenchido, ou envio rápido demais (menos de 3 segundos)
$t = (int)campo('t', 15);
if (campo('site', 50) !== '' || ($t > 0 && (microtime(true) * 1000 - $t) < 3000)) { header('Location: ' . $ok, true, 303); exit; }

$tipo = campo('tipo', 12);
$c = array(
  'quando' => gmdate('Y-m-d H:i', time() + 3600),
  'tipo' => isset($TIPOS[$tipo]) ? $tipo : 'outro',
  'nome' => campo('nome', 80),
  'email' => campo('email', 100),
  'whatsapp' => campo('whatsapp', 25),
  'pais' => campo('pais', 40),
  'link' => campo('link', 120),
  'mensagem' => campo('mensagem', 1500, true),
  'origem' => preg_match('/^[a-z0-9]{2,16}$/', campo('de', 16)) ? campo('de', 16) : '',
);
if (mb_strlen($c['nome'], 'UTF-8') < 2 || !filter_var($c['email'], FILTER_VALIDATE_EMAIL) || mb_strlen($c['mensagem'], 'UTF-8') < 10 || campo('aceito', 2) !== '1') {
  header('Location: /contato/', true, 303); exit;
}
// limite simples: no máximo 40 contatos por dia (proteção contra spam em massa)
$dir = dirname(__DIR__) . '/contador/dados';
if (!is_dir($dir)) @mkdir($dir, 0755, true);
$arq = $dir . '/contatos.jsonl';
$hoje = substr($c['quando'], 0, 10); $n = 0;
if (is_file($arq)) { foreach (file($arq, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $ln) { if (strpos($ln, '"quando":"' . $hoje) !== false) $n++; } }
if ($n >= 40) { header('Location: ' . $ok, true, 303); exit; }
@file_put_contents($arq, json_encode($c, JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);

// e-mail para a Loja
$assunto = '[' . $TIPOS[$c['tipo']] . '] ' . $c['nome'] . ' · contato pelo site';
$corpo = "Novo contato pelo site da Loja do Imigrante\n\n"
  . "Assunto: " . $TIPOS[$c['tipo']] . "\n"
  . "Nome: " . $c['nome'] . "\n"
  . "E-mail: " . $c['email'] . "\n"
  . "WhatsApp: " . ($c['whatsapp'] !== '' ? $c['whatsapp'] : '–') . "\n"
  . "País: " . ($c['pais'] !== '' ? $c['pais'] : '–') . "\n"
  . ($c['link'] !== '' ? "Perfil/site: " . $c['link'] . "\n" : '')
  . ($c['origem'] !== '' ? "Veio de: " . strtoupper($c['origem']) . "\n" : '')
  . "Data: " . $c['quando'] . " (hora de Portugal)\n\n"
  . "Mensagem:\n" . $c['mensagem'] . "\n\n"
  . "Para responder, é só clicar em Responder: a resposta vai direto para " . $c['email'] . ".\n";
$enc = function ($s) { return '=?UTF-8?B?' . base64_encode($s) . '?='; };
$cab = "From: " . $enc('Site Loja do Imigrante') . " <" . $DE_SITE . ">\r\n"
  . "Reply-To: " . $enc($c['nome']) . " <" . $c['email'] . ">\r\n"
  . "MIME-Version: 1.0\r\n"
  . "Content-Type: text/plain; charset=UTF-8\r\n"
  . "Content-Transfer-Encoding: 8bit\r\n";
@mail($PARA, $enc($assunto), $corpo, $cab, '-f' . $DE_SITE);

header('Location: ' . $ok, true, 303);
