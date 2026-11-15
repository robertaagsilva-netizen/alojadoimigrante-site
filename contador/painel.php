<?php
// Painel do contador. Abre só com a chave certa: painel.php?k=CHAVE
$HASH = '488e2285613a4c99ffda09ee14d6962329c0ccf4adf238a1377df640ee9ec7e0';
$k = isset($_GET['k']) ? $_GET['k'] : '';
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');
if (!hash_equals($HASH, hash('sha256', $k))) { http_response_code(404); echo 'Página não encontrada.'; exit; }

$file = __DIR__ . '/dados/contagens.json';
$data = is_file($file) ? json_decode(file_get_contents($file), true) : array();
if (!is_array($data)) $data = array();
krsort($data);

$hoje = gmdate('Y-m-d', time() + 3600);
function soma($data, $dias, $hoje) {
  $lim = date('Y-m-d', strtotime($hoje . ' -' . ($dias - 1) . ' days'));
  $t = array();
  foreach ($data as $d => $ev) { if ($d >= $lim && $d <= $hoje) foreach ($ev as $e => $n) $t[$e] = (isset($t[$e]) ? $t[$e] : 0) + $n; }
  return $t;
}
$per = isset($_GET['p']) ? max(1, min(400, intval($_GET['p']))) : 7;
$T = soma($data, $per, $hoje);
function v($T, $e) { return isset($T[$e]) ? $T[$e] : 0; }
function pref($T, $p) { $s = 0; foreach ($T as $e => $n) if (strpos($e, $p) === 0) $s += $n; return $s; }

$L = array(
  'site_abriu' => 'Abriram a página de links (bio)',
  'calc_abriu' => 'Abriram a calculadora',
  'calc_vindo_bio' => '… pelo link curto /calculadora',
  'calc_pais_pt' => 'Escolheram Portugal',
  'calc_pais_es' => 'Escolheram Espanha',
  'calc_pais_fora' => 'Escolheram "ainda não moro"',
  'calc_resultado_pt_perm' => 'Viram a data: residência permanente PT',
  'calc_resultado_es_arr' => 'Viram a data: arraigo ES',
  'calc_resultado_es_nac' => 'Viram a data: nacionalidade ES',
  'calc_mudou_data' => 'Digitaram a própria data',
  'calc_quero_checklist' => 'Clicaram "Quero o checklist completo" (viram o preço)',
  'calc_pagar_checklist' => 'Foram para o pagamento do checklist (9,90 €)',
  'calc_pagar_consultoria' => 'Foram para o pagamento da consultoria (35 €)',
  'calc_whatsapp' => 'Clicaram no WhatsApp',
  'site_calculadora' => 'Clicaram no botão da calculadora',
  'site_ferramentas' => 'Clicaram no botão das ferramentas de PDF',
  'site_pagar_consultoria' => 'Clicaram em Agendar consultoria (35 €)',
  'site_pagar_checklist' => 'Clicaram no checklist (9,90 €)',
  'site_whatsapp' => 'Clicaram no WhatsApp',
  'ferr_whatsapp' => 'Clicaram no WhatsApp (ferramentas)',
  'link_checklist' => 'Link curto /checklist (foi para o pagamento)',
  'link_consultoria' => 'Link curto /consultoria (foi para o pagamento)',
  'ferr_abriu' => 'Abriram as ferramentas de PDF',
  'ferr_fotos_pdf' => 'Geraram PDF de fotos',
  'ferr_juntar' => 'Juntaram PDFs',
  'ferr_assinar' => 'Assinaram um PDF',
  'ferr_comprimir' => 'Comprimiram um PDF',
);
?><!doctype html>
<html lang="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>Contador · Loja do Imigrante</title>
<style>
:root{--bg:#12110f;--card:#1d1b18;--tx:#f4eedf;--mut:#a9a192;--gold:#ffd34d}
body{margin:0;background:var(--bg);color:var(--tx);font-family:system-ui,sans-serif;padding:16px}
main{max-width:640px;margin:0 auto}
h1{font-size:20px;margin:4px 0 12px}h2{font-size:15px;color:var(--gold);margin:22px 0 8px;text-transform:uppercase;letter-spacing:.04em}
.tabs a{display:inline-block;padding:7px 12px;border-radius:99px;background:var(--card);color:var(--tx);text-decoration:none;margin:0 6px 6px 0;font-size:14px}
.tabs a.on{background:var(--gold);color:#1a1500;font-weight:700}
table{width:100%;border-collapse:collapse;background:var(--card);border-radius:12px;overflow:hidden}
td{padding:10px 12px;border-bottom:1px solid #2b2824;font-size:14px}td.n{text-align:right;font-weight:700;font-size:16px;white-space:nowrap}
.big{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}.big div{background:var(--card);border-radius:12px;padding:12px}.big b{display:block;font-size:26px;color:var(--gold)}.big span{font-size:13px;color:var(--mut)}
p.note{color:var(--mut);font-size:13px}
</style></head><body><main>
<h1>Contador da Loja do Imigrante</h1>
<div class="tabs">
<?php foreach (array(1 => 'Hoje', 7 => '7 dias', 30 => '30 dias', 400 => 'Tudo') as $d => $t) echo '<a class="' . ($d == $per ? 'on' : '') . '" href="?k=' . htmlspecialchars($k) . '&p=' . $d . '">' . $t . '</a>'; ?>
</div>
<div class="big">
  <div><b><?= v($T, 'calc_abriu') ?></b><span>abriram a calculadora</span></div>
  <div><b><?= pref($T, 'calc_resultado_') ?></b><span>chegaram até a data</span></div>
  <div><b><?= v($T, 'calc_quero_checklist') ?></b><span>viram o preço do checklist</span></div>
  <div><b><?= v($T, 'calc_pagar_checklist') + v($T, 'link_checklist') ?></b><span>foram para o pagamento do checklist</span></div>
</div>
<p class="note">"Abriram" conta uma vez por visita. Ir para o pagamento não quer dizer que pagou: as vendas confirmadas estão no Stripe.</p>
<?php
$grupos = array('Calculadora' => 'calc_', 'Página de links e links curtos' => array('site_', 'link_'), 'Ferramentas de PDF' => 'ferr_');
foreach ($grupos as $g => $ps) {
  $ps = (array)$ps; $rows = '';
  foreach ($T as $e => $n) { foreach ($ps as $p) if (strpos($e, $p) === 0) { $rows .= '<tr><td>' . htmlspecialchars(isset($L[$e]) ? $L[$e] : str_replace('_', ' ', $e)) . '</td><td class="n">' . $n . '</td></tr>'; } }
  echo '<h2>' . $g . '</h2>' . ($rows ? '<table>' . $rows . '</table>' : '<p class="note">Nada ainda neste período.</p>');
}
?>
<h2>Dia a dia: calculadora</h2>
<table><?php $i = 0; foreach ($data as $d => $ev) { if ($i++ >= 14) break;
  echo '<tr><td>' . date('d/m', strtotime($d)) . '</td><td class="n">' . (isset($ev['calc_abriu']) ? $ev['calc_abriu'] : 0) . ' abriram · ' . (isset($ev['calc_quero_checklist']) ? $ev['calc_quero_checklist'] : 0) . ' viram preço</td></tr>'; } ?></table>
</main></body></html>
