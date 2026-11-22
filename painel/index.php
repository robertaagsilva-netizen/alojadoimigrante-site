<?php
// Painel da Loja do Imigrante: contatos (ManyChat), vendas (Stripe) e visitas (contador).
// Abre só com a chave do contador: /painel/?k=CHAVE
date_default_timezone_set('Europe/Madrid');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');
$HASH = '488e2285613a4c99ffda09ee14d6962329c0ccf4adf238a1377df640ee9ec7e0';
$k = isset($_REQUEST['k']) ? $_REQUEST['k'] : '';
if (!hash_equals($HASH, hash('sha256', $k))) { http_response_code(404); echo 'Página não encontrada.'; exit; }

$DIR = __DIR__ . '/dados';
if (!is_dir($DIR)) @mkdir($DIR, 0755, true);
$CFG_FILE = $DIR . '/config.json';
$cfg = is_file($CFG_FILE) ? json_decode(file_get_contents($CFG_FILE), true) : array();
if (!is_array($cfg)) $cfg = array();
function h($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
$base = '?k=' . rawurlencode($k);

// ---------- configuração da chave do Stripe ----------
$msg = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  if (isset($_POST['remover'])) { unset($cfg['stripe']); $msg = 'Chave removida.'; }
  else {
    $sk = trim(isset($_POST['stripe']) ? $_POST['stripe'] : '');
    if (preg_match('/^(rk|sk)_(live|test)_[A-Za-z0-9]{10,}$/', $sk)) { $cfg['stripe'] = $sk; @unlink($DIR . '/stripe_cache.json'); $msg = 'Chave salva.'; }
    else $msg = 'Essa chave não parece certa. Ela começa com rk_live_.';
  }
  file_put_contents($CFG_FILE, json_encode($cfg));
  @chmod($CFG_FILE, 0600);
}
$config = isset($_GET['config']) || empty($cfg['stripe']);

// ---------- período ----------
$per = isset($_GET['p']) ? intval($_GET['p']) : 7;
if (!in_array($per, array(1, 7, 30))) $per = 7;
$ini = strtotime('today') - ($per - 1) * 86400;

// ---------- contatos do ManyChat ----------
$leads = array();
$lf = $DIR . '/contatos.jsonl';
if (is_file($lf)) foreach (file($lf, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $ln) { $x = json_decode($ln, true); if (is_array($x) && $x['quando'] >= $ini) $leads[] = $x; }
usort($leads, function ($a, $b) { return $b['quando'] - $a['quando']; });

// ---------- vendas do Stripe ----------
$pagos = array(); $parados = array(); $erroStripe = '';
if (!empty($cfg['stripe'])) {
  $cache = $DIR . '/stripe_cache.json'; $sess = null;
  if (is_file($cache)) { $c = json_decode(file_get_contents($cache), true); if ($c && $c['p'] == $per && time() - $c['t'] < 300 && !isset($_GET['atualizar'])) $sess = $c['d']; }
  if ($sess === null) {
    $url = 'https://api.stripe.com/v1/checkout/sessions?limit=100&created[gte]=' . $ini . '&expand[]=data.line_items';
    $ch = curl_init($url);
    curl_setopt_array($ch, array(CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 15, CURLOPT_USERPWD => $cfg['stripe'] . ':'));
    $r = curl_exec($ch); $code = curl_getinfo($ch, CURLINFO_HTTP_CODE); curl_close($ch);
    $j = json_decode($r, true);
    if ($code == 200 && isset($j['data'])) { $sess = $j['data']; file_put_contents($cache, json_encode(array('t' => time(), 'p' => $per, 'd' => $sess))); }
    else { $sess = array(); $erroStripe = isset($j['error']['message']) ? $j['error']['message'] : 'Não consegui falar com o Stripe.'; }
  }
  foreach ($sess as $s) {
    $cd = isset($s['customer_details']) && is_array($s['customer_details']) ? $s['customer_details'] : array();
    $item = isset($s['line_items']['data'][0]['description']) ? $s['line_items']['data'][0]['description'] : 'Pagamento';
    $row = array('quando' => $s['created'], 'nome' => isset($cd['name']) ? $cd['name'] : '', 'email' => isset($cd['email']) ? $cd['email'] : '',
      'item' => $item, 'valor' => $s['amount_total'] / 100);
    if ($s['payment_status'] === 'paid') $pagos[] = $row;
    elseif ($row['email'] !== '') $parados[] = $row;
  }
}
$faturado = 0; foreach ($pagos as $p) $faturado += $p['valor'];

// ---------- contador do site ----------
$cont = array(); $cf = dirname(__DIR__) . '/contador/dados/contagens.json';
$cd = is_file($cf) ? json_decode(file_get_contents($cf), true) : array();
if (is_array($cd)) foreach ($cd as $d => $ev) if (strtotime($d) >= $ini) foreach ($ev as $e => $n) $cont[$e] = (isset($cont[$e]) ? $cont[$e] : 0) + $n;
$c = function ($e) use ($cont) { return isset($cont[$e]) ? $cont[$e] : 0; };
$visitas = $c('ckpag_abriu') + $c('orient_abriu');
$cliques = $c('ckpag_comprar') + $c('orient_comprar');

// ---------- quem precisa de atenção ----------
$atencao = array();
foreach ($parados as $p) $atencao[] = array('quando' => $p['quando'], 'quem' => $p['nome'] ?: $p['email'], 'det' => 'Começou a pagar ' . $p['item'] . ' e não terminou · ' . $p['email'], 'acao' => 'mandar e-mail');
$compradores = array_map(function ($p) { return mb_strtolower($p['nome']); }, $pagos);
$quentes = array('AJUDA', 'CONSULTORIA', 'FAMÍLIA', 'FAMILIA', 'CASAR', 'CASAMENTO', 'FRANÇA', 'FRANCA', 'KIT');
foreach ($leads as $l) {
  if (!in_array($l['palavra'], $quentes) || time() - $l['quando'] < 86400) continue;
  if ($l['nome'] !== '' && in_array(mb_strtolower($l['nome']), $compradores)) continue;
  $atencao[] = array('quando' => $l['quando'], 'quem' => $l['nome'] ?: '@' . $l['usuario'], 'det' => 'Comentou ' . $l['palavra'] . ' há mais de 1 dia e ainda não comprou' . ($l['usuario'] ? ' · @' . $l['usuario'] : ''), 'acao' => 'chamar no direct');
}
usort($atencao, function ($a, $b) { return $b['quando'] - $a['quando']; });
$atencao = array_slice($atencao, 0, 15);

$DIAS = array('dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sáb');
function quando($t) { global $DIAS; return (date('Y-m-d', $t) === date('Y-m-d') ? 'hoje' : $DIAS[date('w', $t)] . ' ' . date('d/m', $t)) . ' ' . date('H:i', $t); }
function euro($v) { return number_format($v, 2, ',', '.') . ' €'; }
$hora = intval(date('G')); $ola = $hora < 12 ? 'Bom dia' : ($hora < 20 ? 'Boa tarde' : 'Boa noite');
?><!doctype html>
<html lang="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>Painel · Loja do Imigrante</title>
<link rel="icon" href="../logo.png">
<style>
:root{--bg:#12110f;--card:#1c1a17;--line:#34302a;--tx:#f4eedf;--mut:#a9a192;--gold:#ffd34d;--ink:#1a1405;--ok:#25d366;--warn:#ff8a5c}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;padding:20px 16px 48px}
main{max-width:980px;margin:0 auto;display:grid;gap:16px}
header{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between}
h1{font-size:22px;margin:0}
.sub{color:var(--mut);font-size:13px}
.per{display:flex;gap:6px}
.per a{color:var(--tx);text-decoration:none;border:1px solid var(--line);border-radius:99px;padding:6px 12px;font-size:13px}
.per a.on{background:var(--gold);color:var(--ink);border-color:var(--gold);font-weight:700}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px}
.kpi small{display:block;color:var(--mut);font-size:12px}
.kpi b{font-size:26px;font-variant-numeric:tabular-nums}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}
.box{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;min-height:120px}
.box.att{border-color:var(--warn)}
.box h2{font-size:15px;margin:0 0 10px;display:flex;justify-content:space-between}
.box h2 span{background:var(--line);border-radius:99px;padding:0 9px;font-size:12px;line-height:22px}
.row{display:flex;justify-content:space-between;gap:10px;padding:8px 0;border-top:1px solid var(--line)}
.row:first-of-type{border-top:0}
.row div{min-width:0}
.row b{display:block;font-size:14px}
.row small{color:var(--mut);font-size:12px;display:block;overflow-wrap:anywhere}
.pill{white-space:nowrap;align-self:center;font-size:12px;border-radius:99px;padding:2px 9px;font-weight:600}
.p-t{background:#26314a;color:#9fb6ff}.p-ok{background:#123d24;color:var(--ok)}.p-w{background:#40220f;color:var(--warn)}
.vazio{color:var(--mut);font-size:13px;margin:6px 0 0}
.erro{background:#40220f;border:1px solid var(--warn);border-radius:10px;padding:10px 12px;font-size:14px}
.ok{background:#123d24;border:1px solid var(--ok);border-radius:10px;padding:10px 12px;font-size:14px}
form.cfg{display:grid;gap:10px}
input[type=password]{width:100%;padding:12px;border-radius:10px;border:1px solid var(--line);background:#0d0c0b;color:var(--tx);font-size:15px}
button{padding:12px;border-radius:10px;border:0;background:var(--gold);color:var(--ink);font-weight:700;font-size:15px;cursor:pointer}
button.sec{background:transparent;color:var(--mut);border:1px solid var(--line)}
ol{padding-left:20px;margin:6px 0}ol li{margin:4px 0}
footer{color:var(--mut);font-size:12px;display:flex;flex-wrap:wrap;gap:14px}
a{color:var(--gold)}
</style></head><body><main>
<header>
  <div><h1><?= $ola ?>, Roberta ☀️</h1><div class="sub">Atualizado <?= date('d/m H:i') ?> · vendas do Stripe atualizam a cada 5 min</div></div>
  <nav class="per"><?php foreach (array(1 => 'Hoje', 7 => '7 dias', 30 => '30 dias') as $n => $t) echo '<a class="' . ($n == $per ? 'on' : '') . '" href="' . $base . '&p=' . $n . '">' . $t . '</a>'; ?></nav>
</header>
<?php if ($msg) echo '<div class="ok">' . h($msg) . '</div>'; ?>
<?php if ($erroStripe) echo '<div class="erro">Stripe: ' . h($erroStripe) . ' <a href="' . $base . '&config=1">Ver a chave</a></div>'; ?>

<?php if ($config): ?>
<section class="box">
  <h2>Ligar o Stripe ao painel</h2>
  <ol>
    <li>No Stripe, abra <b>Desenvolvedores → Chaves de API</b> e toque em <b>Criar chave restrita</b>.</li>
    <li>Nome: <b>Painel Loja</b>. Em <b>Checkout Sessions</b>, marque <b>Leitura</b>. Deixe todo o resto em <b>Nenhuma</b>.</li>
    <li>Crie a chave, copie (começa com <b>rk_live_</b>) e cole aqui:</li>
  </ol>
  <form class="cfg" method="post" action="<?= $base ?>">
    <input type="password" name="stripe" placeholder="rk_live_..." autocomplete="off" required>
    <button>Salvar chave</button>
  </form>
  <?php if (!empty($cfg['stripe'])): ?>
  <form class="cfg" method="post" action="<?= $base ?>" style="margin-top:10px"><button class="sec" name="remover" value="1">Remover a chave salva</button></form>
  <?php endif; ?>
  <p class="vazio">A chave fica guardada só no servidor do site, com leitura apenas. Ela não consegue cobrar nem devolver dinheiro.</p>
</section>
<?php endif; ?>

<section class="kpis">
  <div class="kpi"><small>Contatos novos</small><b><?= count($leads) ?></b></div>
  <div class="kpi"><small>Vendas</small><b><?= count($pagos) ?></b></div>
  <div class="kpi"><small>Faturado</small><b><?= euro($faturado) ?></b></div>
  <div class="kpi"><small>Visitas às páginas de venda</small><b><?= $visitas ?></b></div>
  <div class="kpi"><small>Cliques em comprar</small><b><?= $cliques ?></b></div>
</section>

<section class="cols">
  <div class="box"><h2>Quem chegou <span><?= count($leads) ?></span></h2>
    <?php foreach (array_slice($leads, 0, 30) as $l): ?>
      <div class="row"><div><b><?= h($l['nome'] ?: '@' . $l['usuario']) ?></b><small><?= h($l['palavra']) ?> · <?= h($l['canal']) ?><?= $l['usuario'] ? ' · @' . h($l['usuario']) : '' ?></small></div><span class="pill p-t"><?= quando($l['quando']) ?></span></div>
    <?php endforeach; if (!$leads) echo '<p class="vazio">Ninguém comentou uma palavra-chave neste período.</p>'; ?>
  </div>
  <div class="box"><h2>Quem comprou <span><?= count($pagos) ?></span></h2>
    <?php foreach ($pagos as $p): ?>
      <div class="row"><div><b><?= h($p['nome'] ?: $p['email']) ?></b><small><?= h($p['item']) ?> · <?= quando($p['quando']) ?></small></div><span class="pill p-ok"><?= euro($p['valor']) ?> pago</span></div>
    <?php endforeach; if (!$pagos) echo '<p class="vazio">' . (empty($cfg['stripe']) ? 'Ligue o Stripe para ver as vendas.' : 'Nenhuma venda neste período ainda.') . '</p>'; ?>
  </div>
  <div class="box att"><h2>Precisa de atenção <span><?= count($atencao) ?></span></h2>
    <?php foreach ($atencao as $a): ?>
      <div class="row"><div><b><?= h($a['quem']) ?></b><small><?= h($a['det']) ?></small></div><span class="pill p-w"><?= h($a['acao']) ?></span></div>
    <?php endforeach; if (!$atencao) echo '<p class="vazio">Tudo em dia. 💛</p>'; ?>
  </div>
</section>

<footer>
  <a href="<?= $base ?>&p=<?= $per ?>&atualizar=1">Atualizar vendas agora</a>
  <a href="../contador/painel.php?k=<?= rawurlencode($k) ?>&p=<?= $per ?>">Contador detalhado do site</a>
  <a href="<?= $base ?>&config=1">Chave do Stripe</a>
</footer>
</main></body></html>
