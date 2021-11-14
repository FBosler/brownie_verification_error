const ipfs = require('nano-ipfs-store').at('https://ipfs.infura.io:5001')

;(async () => {
    const doc = JSON.stringify({
        name: 'sunset',
        description: 'beautiful sunset',
        image: "https://ipfs.io/ipfs/QmeA4sYSdETummDikc3XkYddzSackQeyiFdG81iS3DLVFK?filename=sunset.jpeg",
        attributes: [
            {
                trait_type: "sun level",
                value: 45
            },
            {
                trait_type: "water level",
                value: 85
            }
        ]
    })

    const cid = await ipfs.add(doc)

    console.log('IPFS cid:', cid)

    console.log(await ipfs.cat(cid))
})()
