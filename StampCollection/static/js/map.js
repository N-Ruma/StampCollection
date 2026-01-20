map = L.map('map', {
  minZoom: 13,
  maxZoom: 17,
  maxBounds: [
    [42.25, 140.90], // 南西
    [42.39, 141.05]  // 北東
  ],
  maxBoundsViscosity: 1.0
});

map.setView([42.316, 140.99], 14);

// --- OpenStreetMapタイルを読み込み ---
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

// --- 現在地の取得と表示 ---
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;

      const currentMarker = L.marker([lat, lng])
        .addTo(map)
        .bindPopup("📍 現在地")
        .openPopup();

      map.setView([lat, lng], 14);
    },
    (error) => {
      console.warn("位置情報を取得できませんでした。デフォルト位置を使用します。");
    }
  );
} else {
  alert("このブラウザは位置情報に対応していません。");
}

// --- 観光スポット設定 ---
const spots = [
  { 
    name: "地球岬", 
    lat: 42.2969, 
    lng: 140.9812,
    url: "http://muro-kanko.com/see/chikyuumisaki.html"
  },
  { 
    name: "室蘭八幡宮", 
    lat: 42.3203, 
    lng: 140.9767,
    url: "https://hokkaidojinjacho.jp/%e5%ae%a4%e8%98%ad%e5%85%ab%e5%b9%a1%e5%ae%ae/"
  },
  { 
    name: "白鳥大橋展望台", 
    lat: 42.3472, 
    lng: 141.0083,
    url: "http://muro-kanko.com/night/hakuchouoohashi.html"
  }
];

// --- 各スポットにマーカーを追加 ---
spots.forEach(spot => {
  const marker = L.marker([spot.lat, spot.lng]).addTo(map);

  // マウスオーバーでポップアップ表示
  marker.on('mouseover', () => {
    marker.bindPopup(`<b>${spot.name}</b><br>クリックで詳細を見る`).openPopup();
  });

  // クリックで観光サイトへ遷移
  marker.on('click', () => {
    const confirmJump = confirm(`${spot.name} の観光ページを開きますか？`);
    if (confirmJump) {
      window.open(spot.url, '_blank'); // 新しいタブで開く
    }
  });
});

// --- スタンプ追加用（地図クリック） ---
let addMarker = null;

map.on('click', function (e) {
  const lat = e.latlng.lat;
  const lng = e.latlng.lng;

  // すでに仮ピンがあれば削除
  if (addMarker) {
    map.removeLayer(addMarker);
  }

  // 新しいピンを立てる
  addMarker = L.marker([lat, lng]).addTo(map);

  // hidden input に緯度・経度をセット
  document.getElementById('latitude').value = lat;
  document.getElementById('longitude').value = lng;

  // フォームを表示
  document.getElementById('stamp-form').style.display = 'block';
});

// --- キャンセルボタン処理 ---
document.getElementById('cancel-add').addEventListener('click', () => {
  if (addMarker) {
    map.removeLayer(addMarker);
    addMarker = null;
  }
  document.getElementById('stamp-form').style.display = 'none';
});
